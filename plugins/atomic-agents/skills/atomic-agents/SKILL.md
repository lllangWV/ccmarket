---
name: atomic-agents
description: Use when building AI agents with the atomic-agents Python library, referencing AtomicAgent, BaseIOSchema, BaseTool, or working with atomic-agents examples
---

# Atomic Agents Framework

## Overview

Atomic Agents is a lightweight Python framework for building modular AI agent pipelines. Built on Instructor and Pydantic, it enables strongly-typed, composable agents with explicit Python control flow.

**Core principle:** Each component (agent, tool, context provider) has a single responsibility and explicit typed interfaces.

## Quick Reference

### Imports

```python
# Core classes
from atomic_agents import (
    AtomicAgent,      # Main agent class
    AgentConfig,      # Agent configuration
    BaseIOSchema,     # Base for all input/output schemas
    BaseTool,         # Base for tools
    BaseToolConfig,   # Tool configuration
)

# Context management
from atomic_agents.context import (
    SystemPromptGenerator,        # Builds system prompts
    ChatHistory,                  # Conversation memory
    BaseDynamicContextProvider,   # Dynamic context injection
)

# LLM client (required)
import instructor
import openai
```

### Agent Pattern

```python
class MyInputSchema(BaseIOSchema):
    """Input description."""
    query: str = Field(..., description="Clear description for LLM")

class MyOutputSchema(BaseIOSchema):
    """Output description."""
    answer: str = Field(..., description="What the LLM should produce")

agent = AtomicAgent[MyInputSchema, MyOutputSchema](
    AgentConfig(
        client=instructor.from_openai(openai.OpenAI()),
        model="gpt-4o-mini",
        system_prompt_generator=SystemPromptGenerator(
            background=["Agent role and expertise"],
            steps=["Step 1", "Step 2"],
            output_instructions=["How to fill output fields"],
        ),
    )
)

result = agent.run(MyInputSchema(query="..."))
```

### Tool Pattern

```python
class MyToolInput(BaseIOSchema):
    url: str = Field(..., description="URL to process")

class MyToolOutput(BaseIOSchema):
    content: str = Field(..., description="Extracted content")
    error: str | None = Field(None, description="Error if failed")

class MyToolConfig(BaseToolConfig):
    timeout: int = 10

class MyTool(BaseTool[MyToolInput, MyToolOutput]):
    def run(self, input: MyToolInput) -> MyToolOutput:
        try:
            # Implementation
            return MyToolOutput(content="...")
        except Exception as e:
            return MyToolOutput(content="", error=str(e))
```

### Context Provider Pattern

```python
class MyContextProvider(BaseDynamicContextProvider):
    def __init__(self, title: str):
        super().__init__(title=title)
        self.data: list[str] = []

    def get_info(self) -> str:
        if not self.data:
            return "No data available."
        return "\n".join(self.data)

# Register with agent
agent.register_context_provider("my_context", provider)
```

### Schema Chaining

Align agent output with tool input for seamless composition:

```python
# Agent output matches tool input schema
agent = AtomicAgent[UserQuery, SearchToolInputSchema](...)
result = agent.run(user_input)
search_results = search_tool.run(result)  # Direct pass-through
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `from atomic_agents.lib...` | Use `from atomic_agents import ...` |
| `from atomic_agents.agents.base_agent import BaseAgent` | Use `AtomicAgent` from top-level |
| Using `BaseModel` for schemas | Use `BaseIOSchema` |
| `openai.OpenAI()` directly | Wrap with `instructor.from_openai()` |
| Raising exceptions in tools | Return error field in output schema |
| Missing Field descriptions | Always add `description="..."` for LLM guidance |

## Debugging Checklist

1. **Empty/wrong outputs** → Check Field descriptions are clear for LLM
2. **Schema validation errors** → Ensure input/output types match
3. **Agent not following instructions** → Improve SystemPromptGenerator `output_instructions`
4. **Tool integration fails** → Verify schema alignment between agent output and tool input
