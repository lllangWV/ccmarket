#!/usr/bin/env python3
"""
Minimal coding agent in ~100 lines.
Demonstrates the core loop with read_file, list_files, bash, and edit_file tools.

Usage:
    export ANTHROPIC_API_KEY=your-key
    python3 agent.py
"""

import os
import subprocess
import anthropic

client = anthropic.Anthropic()

TOOLS = [
    {
        "name": "read_file",
        "description": "Read contents of a file. Do not use with directories.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "File path to read"}},
            "required": ["path"]
        }
    },
    {
        "name": "list_files",
        "description": "List files in a directory. Defaults to current directory.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Directory path"}}
        }
    },
    {
        "name": "bash",
        "description": "Execute a bash command and return output.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string", "description": "Command to run"}},
            "required": ["command"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing old_str with new_str. Empty old_str creates new file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_str": {"type": "string"},
                "new_str": {"type": "string"}
            },
            "required": ["path", "old_str", "new_str"]
        }
    }
]


def execute_tool(name: str, inputs: dict) -> str:
    try:
        if name == "read_file":
            with open(inputs["path"]) as f:
                return f.read()
        elif name == "list_files":
            path = inputs.get("path", ".")
            return "\n".join(os.listdir(path))
        elif name == "bash":
            result = subprocess.run(inputs["command"], shell=True, capture_output=True, text=True)
            return result.stdout + result.stderr
        elif name == "edit_file":
            path, old_str, new_str = inputs["path"], inputs["old_str"], inputs["new_str"]
            if old_str == "":
                with open(path, "w") as f:
                    f.write(new_str)
                return f"Created {path}"
            with open(path) as f:
                content = f.read()
            if old_str not in content:
                return f"Error: '{old_str}' not found in {path}"
            with open(path, "w") as f:
                f.write(content.replace(old_str, new_str, 1))
            return f"Edited {path}"
    except Exception as e:
        return f"Error: {e}"


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=messages,
            tools=TOOLS
        )
        
        if response.stop_reason == "end_turn":
            return "".join(b.text for b in response.content if hasattr(b, "text"))
        
        messages.append({"role": "assistant", "content": response.content})
        
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  → {block.name}({block.input})")
                result = execute_tool(block.name, block.input)
                print(f"  ← {result[:200]}{'...' if len(result) > 200 else ''}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })
        
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break
    
    return "".join(b.text for b in response.content if hasattr(b, "text"))


def main():
    print("Minimal Coding Agent (type 'quit' to exit)\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break
        if not user_input:
            continue
        response = run_agent(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
