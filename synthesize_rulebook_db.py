import os
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
    current_section_name: str | None = None
    current_rules: List[Rule] = []

    current_title: str | None = None
    current_condition: str | None = None
    current_action: str | None = None
    current_example: str | None = None

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


async def merge_and_clean_branches(branch_indices: List[int]) -> SingleAgentResponse:
    base_dir = Path("agent_rulebook_db_new_depr")
    rulebooks: List[Rulebook] = []
    for idx in branch_indices:
        path = base_dir / f"rulebook_branch_{idx}.md"
        rb = parse_rulebook_markdown(path)
        rulebooks.append(rb)

    merged_rulebook = merge_rulebooks(rulebooks)
    merged_json = merged_rulebook.model_dump_json(indent=2, ensure_ascii=False)

    schema = SingleAgentResponse.model_json_schema()
    gem = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    agent_prompt = (
        "You are a Rulebook Compiler for a medical appointment scheduling agent.\n\n"
        "You are given a merged rulebook in JSON form, produced by combining multiple branches.\n"
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
    return agent_output


async def main():
    cleaned = await merge_and_clean_branches([1, 2, 3])
    cleaned_json = cleaned.model_dump_json(indent=2, ensure_ascii=False)
    print(cleaned_json)


if __name__ == "__main__":
    asyncio.run(main())
