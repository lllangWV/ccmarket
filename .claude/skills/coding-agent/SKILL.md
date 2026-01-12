---
name: coding-agent
description: Guide for building coding agents from scratch. Use when users want to create their own AI coding assistant, understand how tools like Cursor/Claude Code work internally, implement tool-calling LLM loops, or build custom automation with agentic LLMs. Covers model selection, tool registration, context window management, and the core inference loop.
---

# Building a Coding Agent

A coding agent is **300 lines of code running in a loop with LLM tokens**. The model does the heavy lifting—your job is to wire tools into an inference loop.

## Core Architecture

```
User Input → Allocate to Context → Inference → Check for Tool Call?
                    ↑                              ↓
                    └──────── Tool Result ←── Execute Tool
```

Every coding agent follows this loop:
1. Receive user input (or tool result)
2. Allocate to context window
3. Send for inference
4. Check if response requests tool execution
5. If yes: execute tool, allocate result, go to step 3
6. If no: return response to user

## Model Selection

Not all LLMs are agentic. Models specialize:

| Quadrant | Characteristics | Best For |
|----------|----------------|----------|
| **Agentic** | Biases toward action, chases tool calls | Coding agents (Claude Sonnet, Kimi K2) |
| **Oracle** | Deep reasoning, contemplative | Planning, research, checking work |
| **High Safety** | Ethics-aligned | Consumer applications |
| **Low Safety** | Fewer restrictions | Security research (Grok) |

**For coding agents**: Use Claude Sonnet or Kimi K2. These models are trained to aggressively call tools rather than deliberate.

**For planning/verification**: Wire an Oracle (GPT) as a tool the agentic model can call for guidance.

## Context Window Management

Context windows are small—treat them like a Commodore 64:
- Advertised 200k tokens → ~176k usable (system prompt + harness overhead)
- **Less is more**: More allocation = worse performance
- **One activity per context**: Clear between tasks or outcomes bleed together
- **MCP tool budget**: Each tool consumes tokens. 10 tools × 500 tokens = 5k gone

### MCP Tool Registration

A tool is a function with a billboard:

```json
{
  "name": "read_file",
  "description": "Read contents of a file path. Do not use with directories.",
  "input_schema": {
    "type": "object",
    "properties": {
      "path": { "type": "string", "description": "Relative file path" }
    },
    "required": ["path"]
  }
}
```

The description nudges the model's latent space to invoke that function when relevant.

## Essential Tools (5 Primitives)

Every coding agent needs these five tools. See `references/tools.md` for implementations.

1. **read_file** - Read file contents into context
2. **list_files** - List directory contents
3. **bash** - Execute shell commands
4. **edit_file** - Apply text replacements
5. **code_search** - Search codebase (ripgrep)

## Implementation Steps

### Step 1: Basic Chat Loop

Create a chat loop that sends messages to the LLM and displays responses.

### Step 2: Tool Registration

Register tools with descriptions in the API call. The model will output tool calls in its response when it wants to use them.

### Step 3: Tool Execution Loop

```
while response.has_tool_calls:
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call.name, tool_call.params)
        append_to_context(tool_call, result)
    response = call_llm(context)
```

### Step 4: Harness Prompt

The system prompt configures agent behavior:
- Operating system detection (bash vs PowerShell)
- Working directory
- Tool descriptions and usage guidance
- Output formatting preferences
- Safety guardrails

See `references/harness-prompt.md` for a template.

## Common Pitfalls

1. **Reusing context across tasks** → Outcomes pollute each other
2. **Too many MCP tools** → Context window exhaustion
3. **Wrong model type** → Oracle models won't act, agentic models won't plan
4. **Missing tool descriptions** → Model doesn't know when to call tools
5. **No error handling** → Tool failures crash the loop

## Testing Your Agent

```bash
# Test: Create and verify a file
You: Create fizzbuzz.js and run it

# Expected: Agent calls edit_file, then bash(node fizzbuzz.js)
```

## Further Reading

- `references/tools.md` - Complete tool implementations (Go)
- `references/harness-prompt.md` - System prompt template
- `references/loop.md` - Detailed inference loop with code
