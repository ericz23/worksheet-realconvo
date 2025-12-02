import os
import json

def build_tree(conversations):
    root = {"children": {}, "conv_ids": set()}
    for idx, entry in enumerate(conversations):
        conv = entry["conversation"]
        node = root
        node["conv_ids"].add(idx)
        for turn_index, msg in enumerate(conv):
            key = msg["role"] + "|" + msg["text"]
            if key not in node["children"]:
                node["children"][key] = {
                    "turn_index": turn_index,
                    "role": msg["role"],
                    "text": msg["text"],
                    "children": {},
                    "conv_ids": set()
                }
            node = node["children"][key]
            node["conv_ids"].add(idx)
    return root

def node_to_nested(node):
    children_nested = []
    for child in node["children"].values():
        children_nested.append(node_to_nested(child))
    if "role" not in node:
        return children_nested
    return {
        "turn_index": node["turn_index"],
        "role": node["role"],
        "text": node["text"],
        "conv_ids": sorted(list(node["conv_ids"])),
        "children": children_nested
    }

def main():
    base_dir = "conversation_branches_ft"
    input_path = os.path.join(base_dir, "all_conversations.json")
    output_path = os.path.join(base_dir, "conversation_tree.json")
    with open(input_path, "r", encoding="utf-8") as f:
        conversations = json.load(f)
    root = build_tree(conversations)
    nested = node_to_nested(root)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(nested, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
