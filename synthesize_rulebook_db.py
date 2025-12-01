import os
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Tuple
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()

class Rule(BaseModel):
    title: str
    condition: str
    action: str
    example: str

class Section(BaseModel):
    name: str
    rules: List[Rule]

class Rulebook(BaseModel):
    sections: List[Section]

class SingleAgentResponse(BaseModel):
    rulebook: Rulebook

def parse_rulebook_markdown(path: Path) -> Rulebook:
    text = path.read_text(encoding="utf-8")
    lines = [ln.rstrip("\n") for ln in text.splitlines()]
    sections: List[Section] = []
    current_section_name = None
    current_rules: List[Rule] = []
    current_title = None
    current_condition = None
    current_action = None
    current_example = None
    def flush_rule():
        nonlocal current_title, current_condition, current_action, current_example, current_rules
        if current_title:
            rule = Rule(
                title=current_title.strip(),
                condition=(current_condition or "").strip(),
                action=(current_action or "").strip(),
                example=(current_example or "").strip(),
            )
            current_rules.append(rule)
        current_title = None
        current_condition = None
        current_action = None
        current_example = None
    def flush_section():
        nonlocal current_section_name, current_rules, sections
        if current_section_name and current_rules:
            sections.append(Section(name=current_section_name.strip(), rules=current_rules))
        current_section_name = None
        current_rules = []
    for line in lines:
        if line.startswith("## "):
            flush_rule()
            flush_section()
            current_section_name = line[3:].strip()
        elif line.startswith("### "):
            flush_rule()
            current_title = line[4:].strip()
        elif line.startswith("**When:**"):
            current_condition = line.split("**When:**", 1)[1].strip()
        elif line.startswith("**Action:**"):
            current_action = line.split("**Action:**", 1)[1].strip()
        elif line.startswith("**Example:**"):
            current_example = line.split("**Example:**", 1)[1].strip()
    flush_rule()
    flush_section()
    return Rulebook(sections=sections)

def merge_rulebooks(rulebooks: List[Rulebook]) -> Rulebook:
    sections_by_name: Dict[str, List[Rule]] = {}
    for rb in rulebooks:
        for sec in rb.sections:
            key = sec.name.strip()
            sections_by_name.setdefault(key, [])
            sections_by_name[key].extend(sec.rules)
    merged_sections: List[Section] = []
    for name, rules in sections_by_name.items():
        seen: set[Tuple[str, str, str]] = set()
        unique_rules: List[Rule] = []
        for r in rules:
            k = (r.title.strip(), r.condition.strip(), r.action.strip())
            if k in seen:
                continue
            seen.add(k)
            unique_rules.append(r)
        merged_sections.append(Section(name=name, rules=unique_rules))
    merged_sections.sort(key=lambda s: s.name.lower())
    return Rulebook(sections=merged_sections)

def rulebook_to_markdown(rulebook: Rulebook) -> str:
    lines = ["# Agent Rulebook", ""]
    for section in rulebook.sections:
        lines.append(f"## {section.name}")
        lines.append("")
        for rule in section.rules:
            lines.append(f"### {rule.title}")
            lines.append(f"**When:** {rule.condition}")
            lines.append(f"**Action:** {rule.action}")
            lines.append(f"**Example:** {rule.example}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"

async def merge_rulebook_files(file_paths: List[Path], gem: genai.Client, schema: dict) -> Rulebook:
    rulebooks: List[Rulebook] = []
    for p in file_paths:
        rb = parse_rulebook_markdown(p)
        rulebooks.append(rb)
    merged_rulebook = merge_rulebooks(rulebooks)
    merged_json = merged_rulebook.model_dump_json(indent=2, ensure_ascii=False)
    agent_prompt = (
        "You are a Rulebook Compiler for a medical appointment scheduling agent.\n\n"
        "You are given a merged rulebook in JSON form, produced by combining multiple branches or sub-rulebooks.\n"
        "Your tasks are:\n"
        "- Clean and deduplicate rules while preserving behavior.\n"
        "- Merge overlapping or redundant sections and rules.\n"
        "- Organize the rules hierarchically into clear sections and subsections.\n"
        "- Simplify wording but keep all necessary conditions and actions.\n\n"
        "Return your result as strictly valid JSON that conforms to the SingleAgentResponse schema.\n"
        "Do not include any extra keys, comments, or explanations.\n\n"
        "Merged rulebook JSON:\n"
        f"{merged_json}\n"
    )
    agent_result = await asyncio.to_thread(
        gem.models.generate_content,
        model="gemini-2.5-flash",
        contents=agent_prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": schema,
        },
    )
    agent_output = SingleAgentResponse.model_validate_json(agent_result.text)
    return agent_output.rulebook

async def process_node(node: dict, base_dir: Path, gem: genai.Client, schema: dict) -> Path:
    children = node.get("children", [])
    child_paths: List[Path] = []
    for child in children:
        child_path = await process_node(child, base_dir, gem, schema)
        if child_path not in child_paths:
            child_paths.append(child_path)
    conv_ids = sorted(node["conv_ids"])
    one_based_ids = [i + 1 for i in conv_ids]
    if len(conv_ids) == 1 and not child_paths:
        leaf_id = one_based_ids[0]
        leaf_path = base_dir / f"rulebook_branch_{leaf_id}.md"
        return leaf_path
    fname = "rulebook_branch_" + "_".join(str(i) for i in one_based_ids) + ".md"
    out_path = base_dir / fname
    if out_path.exists():
        return out_path
    if child_paths:
        source_paths = child_paths
    else:
        source_paths = [base_dir / f"rulebook_branch_{i}.md" for i in one_based_ids]
    print("Merging into", out_path.name, "from:", ", ".join(p.name for p in source_paths))
    merged_rulebook = await merge_rulebook_files(source_paths, gem, schema)
    md = rulebook_to_markdown(merged_rulebook)
    out_path.write_text(md, encoding="utf-8")
    return out_path

async def main():
    base_dir = Path("agent_rulebook_db_revised")
    tree_path = Path("conversation_branches") / "conversation_tree.json"
    with tree_path.open("r", encoding="utf-8") as f:
        tree_nodes = json.load(f)
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    schema = SingleAgentResponse.model_json_schema()
    all_conv_ids = set()
    for n in tree_nodes:
        for cid in n["conv_ids"]:
            all_conv_ids.add(cid)
    synthetic_root = {
        "conv_ids": sorted(list(all_conv_ids)),
        "children": tree_nodes
    }
    await process_node(synthetic_root, base_dir, gem, schema)

if __name__ == "__main__":
    asyncio.run(main())