import json
import os
from typing import List, Dict, Any

def load_conversations(json_path: str) -> List[Dict[str, Any]]:
    with open(json_path, 'r') as f:
        return json.load(f)

def build_tree_structure(conversations: List[Dict[str, Any]]) -> Dict[str, Any]:
    tree = {"conversation": [], "children": {}}
    
    for conv_data in conversations:
        conversation = conv_data["conversation"]
        current_node = tree
        
        for i in range(0, len(conversation), 2):
            if i + 1 < len(conversation):
                agent_msg = conversation[i]["text"]
                user_msg = conversation[i + 1]["text"]
                
                key = f"Agent: {agent_msg}\nUser: {user_msg}"
                
                if key not in current_node["children"]:
                    current_node["children"][key] = {
                        "conversation": conversation[:i+2],
                        "children": {}
                    }
                
                current_node = current_node["children"][key]
    
    return tree

def print_tree(node: Dict[str, Any], prefix: str = "", is_last: bool = True):
    if not node["children"]:
        return
    
    children = list(node["children"].items())
    for i, (key, child_node) in enumerate(children):
        is_last_child = i == len(children) - 1
        current_prefix = "└── " if is_last_child else "├── "
        print(f"{prefix}{current_prefix}{key}")
        
        next_prefix = prefix + ("    " if is_last_child else "│   ")
        print_tree(child_node, next_prefix, is_last_child)

def generate_markdown_tree(node: Dict[str, Any], level: int = 0) -> str:
    if not node["children"]:
        return ""
    
    markdown = ""
    for key, child_node in node["children"].items():
        indent = "  " * level
        markdown += f"{indent}- {key}\n"
        markdown += generate_markdown_tree(child_node, level + 1)
    
    return markdown

def main():
    json_path = "conversation_branches/all_conversations.json"
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found. Run get_policy_db.py first.")
        return
    
    conversations = load_conversations(json_path)
    tree = build_tree_structure(conversations)
    
    print("=== Conversation Tree Structure ===")
    print_tree(tree)
    
    markdown_content = "# Conversation Tree\n\n"
    markdown_content += generate_markdown_tree(tree)
    
    os.makedirs("conversation_analysis", exist_ok=True)
    with open("conversation_analysis/tree_visualization.md", "w") as f:
        f.write(markdown_content)
    
    print(f"\nTree visualization saved to conversation_analysis/tree_visualization.md")

if __name__ == "__main__":
    main()