---
name: atomic-agents
description: Helps design, implement, and debug projects built with the Atomic Agents framework, including agents, tools, context providers, and orchestration code. Use when the user is working with the atomic-agents Python library or its examples and wants help writing, refactoring, or troubleshooting agents, tools, schemas, or pipelines.
---

# Implementing Atomic Agents

## Overview

This Skill guides the assistant when helping a user build or maintain projects based on the `atomic-agents` framework from BrainBlend AI. It focuses on designing strongly-typed agents, tools, context providers, and orchestration flows using Atomic Agents’ core abstractions (e.g., `AtomicAgent`, `BaseTool`, `BaseIOSchema`, `BaseDynamicContextProvider`, `SystemPromptGenerator`, `ChatHistory`, `AgentConfig`). :contentReference[oaicite:0]{index=0}  

The Skill assumes the user wants predictable, maintainable agentic pipelines, not open-ended autonomous “do everything” agents.

## When to use this Skill

Trigger this Skill when:

- The user mentions the `atomic-agents` library, Atomic Agents docs, or examples.
- The user references classes like `AtomicAgent`, `AgentConfig`, `BaseIOSchema`, `BaseTool`, `BaseDynamicContextProvider`, `SystemPromptGenerator`, or `ChatHistory`.
- The user is working inside an Atomic Agents–style project layout (e.g., `agents/`, `tools/`, `context_providers.py`, `atomic-examples/`, `deep_research/`).
- The user asks for help creating or modifying agents, tools, context providers, schemas, or orchestration code using Atomic Agents.
- The user wants to adapt one of the official Atomic Agents examples (quickstart, web search agent, deep research, RAG chatbot, etc.) to their own use case. :contentReference[oaicite:1]{index=1}  

Do NOT use this Skill when:

- The user is building agents with a completely different framework (LangChain, CrewAI, AutoGen, custom in-house framework) and does not mention Atomic Agents.
- The user only needs generic prompt engineering help with no code or framework context.
- The user wants a hosted “no-code” agent builder, not Python-based, code-centric workflows.

If the user is mixing frameworks, bias toward treating Atomic Agents as the main orchestration layer and help integrate other pieces into that, rather than trying to replicate Atomic Agents concepts elsewhere.

## Environment and constraints

- **Surfaces**
  - Claude Code / IDE integrations
  - Claude API / Agent SDK
  - Claude in browser when reading GitHub repos, docs, or local files

- **Network**
  - Full network access is assumed for:
    - Reading the Atomic Agents GitHub repo and documentation
    - Reading external APIs or docs referenced by tools (e.g., search APIs, web scraping targets)

- **Packages**
  - Atomic Agents: `atomic-agents` (installed via `pip install atomic-agents` or `uv add atomic-agents`) :contentReference[oaicite:2]{index=2}  
  - LLM providers via Instructor (e.g., `openai`, `groq`, possibly others)
  - `pydantic` for schemas
  - Standard Python tooling (pytest, Black) where relevant

- **Assumptions & guardrails**
  - Always prefer strongly-typed schemas (`BaseIOSchema`) and explicit `AgentConfig` over ad-hoc prompt strings.
  - Keep each agent/tool/context provider **single-responsibility** and composable.
  - Do not fabricate non-existent classes, modules, or config options; cross-check with upstream docs or the user’s repo.
  - Prefer low temperatures (0–0.3) for agents where predictability matters (research, analysis, code generation).
  - Avoid embedding time-sensitive assumptions (exact version numbers, transient model names) into the user’s code unless they explicitly ask.

## Repo helpers

- `examples/tools/base.py` re-exports atomic-agents `BaseTool`/`BaseToolConfig` and
  provides `get_tool_name`, `describe_tool`, and `validate_and_run`.
- `examples/tools/manager.py` discovers atomic-agents tools from
  `examples/tools/builtins` plus any extra paths.
- `examples/tools/ui.py` offers `ToolUIDataAdapter` to format call/result displays
  from tool inputs and outputs.

## Core workflows

### Workflow 1: Understand the user’s Atomic Agents project

Use this whenever you first interact with a new repository or codebase.

1. **Identify project structure**
   - Look for `atomic-agents/`, `atomic-examples/`, or their own package (e.g., `deep_research/`, `agents/`, `tools/`, `context_providers.py`, orchestration scripts like `main.py`). :contentReference[oaicite:3]{index=3}  
2. **Skim key entry points**
   - Open `README.md` or project-level docs.
   - Find any Atomic Agents specific modules (`agents/`, `tools/`, `context_providers.py`, `config.py` or `chat_config.py`, `deep*_` examples).
3. **Detect existing patterns**
   - Note how they construct `AtomicAgent` instances (which provider, model, `SystemPromptGenerator`, and `ChatHistory`).
   - Note naming conventions for schemas (`*InputSchema`, `*OutputSchema`), tools (`*Tool`), and context providers.
4. **Summarize in bullets**
   - Produce a short internal summary of:
     - How agents are currently instantiated.
     - Where tools live.
     - How context providers are registered.
     - Any existing orchestration loop patterns (CLI, TUI, web app, tests).
5. **Align with that style**
   - When proposing changes, follow the user’s existing patterns for imports, naming, directory layout, and testing.

### Workflow 2: Create or extend an Atomic Agent

Use this when the user wants a new agent or to refactor an existing one.

1. **Clarify the agent’s single responsibility**
   - Rephrase the user’s request into one clear job, such as:
     - “Decision agent: decide whether to trigger a search.”
     - “Query agent: generate search queries.”
     - “QA agent: synthesize an answer from context.”
     - “Orchestration agent: route tasks between agents.”
2. **Define input/output schemas**
   - Create two `BaseIOSchema` subclasses in the agent module:
     - `MyAgentInputSchema(BaseIOSchema)`
     - `MyAgentOutputSchema(BaseIOSchema)`
   - Use `Field(..., description="...")` for each field so LLM behavior is clearly constrained and chainable.
3. **Design the system prompt**
   - Use `SystemPromptGenerator` to define:
     - `background`: who the agent is and its domain.
     - `steps`: numbered reasoning steps.
     - `output_instructions`: how to populate the output schema safely and deterministically.
4. **Instantiate the agent**
   - Follow the official pattern for `AtomicAgent` + `AgentConfig`:
     - Use `instructor` to wrap the chosen provider client (e.g., `instructor.from_openai(openai.OpenAI())`).
     - Set `model` and any provider-specific options in `AgentConfig`.
     - Add `history=ChatHistory()` when multi-turn interaction is desired. :contentReference[oaicite:4]{index=4}  
5. **Register context providers**
   - For each dynamic context provider (e.g., scraped content, current date, user profile):
     - Instantiate once in orchestration code.
     - Register on the agent via `agent.register_context_provider("name", provider_instance)`.
6. **Validate with a small test**
   - Create one or more small test calls in a `__main__` guard or tests:
     - Provide a minimal valid input instance.
     - Confirm the agent returns a fully populated output schema with no `None` where fields are required.
   - Adjust schema descriptions and prompt instructions if fields are often missing or misformatted.

### Workflow 3: Create a new tool (BaseTool) and chain it with agents

Use this when the user wants to connect external functionality (search, scraping, APIs, internal services).

1. **Define IO schemas**
   - In the `tools/` module, create:
     - `MyToolInputSchema(BaseIOSchema)`
     - `MyToolOutputSchema(BaseIOSchema)`
   - Keep inputs minimal and explicit (URLs, IDs, flags, etc.).
2. **Define tool config**
   - Create `MyToolConfig(BaseToolConfig)` or similar for configuration that should not come from the LLM directly (API keys, base URLs, timeouts, limits).
3. **Implement the tool**
   - Implement `class MyTool(BaseTool[MyToolInputSchema, MyToolOutputSchema]):`
     - Provide a `run(self, input: MyToolInputSchema) -> MyToolOutputSchema` method.
     - Keep side effects bounded and focused (e.g., just fetch and normalize data).
     - Handle failures gracefully by returning structured `error` fields instead of raising unhandled exceptions.
4. **Support schema chaining**
   - Where possible, design tool input schemas so that an agent’s output schema can be passed directly into `MyTool.run(...)`.
   - Example: a `QueryAgent` whose `OutputSchema` matches `SearXNGSearchToolInputSchema`, so you can call `search_tool.run(agent_output)` without transformation.
5. **Add tests**
   - Write `pytest` tests that:
     - Construct a valid input schema.
     - Call `run`.
     - Assert on structured outputs (shape, basic values, and error handling).
6. **Integrate in orchestration**
   - In the orchestration script/module, compose agents and tools:
     - Agent A → Tool X → Agent B → etc.
   - Keep all control flow explicit in Python, avoiding hidden loops or magical autonomy.

### Workflow 4: Manage dynamic context with context providers

Use this whenever the user wants agents to see shared state (scraped pages, timestamps, etc.) without bloating prompts manually.

1. **Identify context categories**
   - Example: “scraped web pages”, “current date”, “current user/project”, “recent API responses”.
2. **Create context provider classes**
   - Subclass `BaseDynamicContextProvider` for each category.
   - Implement `get_info()` to return a concise, prompt-ready string that is easy for the LLM to parse (including labels, separators, and any needed metadata).
   - Keep providers responsible only for formatting data, not for making decisions.
3. **Manage provider state in orchestration**
   - Instantiate providers once at the top-level (e.g., `ScrapedContentContextProvider("Scraped Content")`).
   - Update their state from orchestration code when new information is available (e.g., after scraping a page).
4. **Register with agents**
   - Register providers with any agents that depend on that context:
     - `agent.register_context_provider("scraped_content", scraped_content_provider)`
     - `agent.register_context_provider("current_date", current_date_provider)`
5. **Ensure clarity and limits**
   - Avoid unbounded context growth:
     - Truncate or summarize long content in `get_info()` if necessary.
     - Consider limiting to the N most recent or most relevant items.
   - Use clear separators and headings in the returned string.

### Workflow 5: Design orchestration flows and CLIs

Use this when wiring multiple agents/tools into an end-to-end flow (e.g., a deep-research pipeline, RAG chatbot, or web search agent). :contentReference[oaicite:5]{index=5}  

1. **Define the control flow in Python**
   - Write a dedicated orchestration module or CLI entry point (e.g., `deep_research/main.py`).
   - Avoid embedding control flow into prompts; keep it in Python functions and loops.
2. **Initialize shared components**
   - Create shared `ChatHistory` if needed.
   - Instantiate context providers and register them with all relevant agents.
   - Instantiate tools (with configs) and any supporting services.
3. **Implement the main loop**
   - Read user input (CLI, API, etc.).
   - For each input:
     - Optionally call a “choice/decision” agent to decide whether to fetch new data.
     - If yes, call a “query” agent → run tools (e.g., search + scrape) → update context providers.
     - Call a QA or synthesis agent to produce the final answer.
   - Return or print structured outputs (including follow-up suggestions if applicable).
4. **Log and monitor**
   - Provide clear logging of:
     - Agent decisions (e.g., whether a new search was triggered).
     - Tool invocations (with inputs, outputs, and any errors).
     - Final outputs.
5. **Refine**
   - Based on observed behavior, refine:
     - Schema descriptions.
     - System prompts (`background`, `steps`, `output_instructions`).
     - Orchestration logic (e.g., thresholds for re-searching, limits on number of pages to scrape).

### Workflow 6: Debugging and refactoring Atomic Agents code

Use this when the user reports errors, inconsistent outputs, or unclear behavior.

1. **Reproduce the issue**
   - Ask for:
     - The relevant agent/tool/context provider code.
     - The exact input schema instance or parameters.
     - Any stack trace or error message.
2. **Check schemas first**
   - Validate `BaseIOSchema` definitions:
     - Are fields required where they should be?
     - Are descriptions clear enough for the LLM?
     - Are there mismatches between an agent’s output and a downstream tool’s input?
3. **Check configuration**
   - Inspect `AgentConfig`:
     - Provider and model name.
     - Temperature and other parameters.
     - Presence/absence of `history` or `system_prompt_generator` where expected.
4. **Check prompts and context providers**
   - Ensure `SystemPromptGenerator` instructions match the schema fields exactly.
   - Check `get_info()` outputs from context providers for unbounded or confusing text.
5. **Isolate components**
   - Run the problematic agent or tool in isolation with a minimal input to see if the issue persists.
   - If it disappears, the problem is likely in orchestration or shared context; otherwise, it’s local to that component.
6. **Refactor toward single responsibility**
   - If a given agent/tool does too many things, propose splitting it into smaller components with clear responsibilities and chain them via schemas.

## Templates and examples

For detailed Skill authoring patterns and general templates, see your existing Skill meta-resources (structure, patterns, checklists, and troubleshooting guidance). :contentReference[oaicite:6]{index=6} :contentReference[oaicite:7]{index=7} :contentReference[oaicite:8]{index=8} :contentReference[oaicite:9]{index=9} :contentReference[oaicite:10]{index=10} :contentReference[oaicite:11]{index=11}  

Below are Atomic Agents–specific code skeletons the assistant should use as defaults when the user asks to “create a new agent/tool/context provider.”

### Agent skeleton

```python
from typing import Any
import instructor
import openai
from pydantic import Field
from atomic_agents import AtomicAgent, AgentConfig, BaseIOSchema
from atomic_agents.context import SystemPromptGenerator, ChatHistory

class MyAgentInputSchema(BaseIOSchema):
    """Short description of what this agent consumes."""
    user_message: str = Field(..., description="The user's natural language request.")

class MyAgentOutputSchema(BaseIOSchema):
    """Short description of what this agent returns."""
    answer: str = Field(..., description="Main answer to the user's request.")
    follow_up_questions: list[str] = Field(
        ..., description="Suggested follow-up questions that deepen the topic."
    )

def build_my_agent() -> AtomicAgent[MyAgentInputSchema, MyAgentOutputSchema]:
    system_prompt_generator = SystemPromptGenerator(
        background=[
            "You are a focused, domain-specific assistant.",
        ],
        steps=[
            "Analyze the user's request.",
            "Use any available context providers to ground your answer.",
            "Produce a clear, concise answer.",
            "Propose 3–5 helpful follow-up questions.",
        ],
        output_instructions=[
            "Always fill in all fields of MyAgentOutputSchema.",
            "Do not invent sources or facts that are not supported by context.",
        ],
    )

    client = instructor.from_openai(openai.OpenAI())

    return AtomicAgent[MyAgentInputSchema, MyAgentOutputSchema](
        config=AgentConfig(
            client=client,
            model="gpt-5-mini",
            system_prompt_generator=system_prompt_generator,
            history=ChatHistory(),
            model_api_parameters={"temperature": 0.1},
        )
    )
````

### Tool skeleton

```python
from typing import Optional
from pydantic import Field, HttpUrl
from atomic_agents import BaseIOSchema, BaseTool, BaseToolConfig

class MyToolInputSchema(BaseIOSchema):
    """Input for the tool."""
    url: HttpUrl = Field(..., description="The URL to process.")

class MyToolOutputSchema(BaseIOSchema):
    """Normalized tool output."""
    content: str = Field(..., description="Extracted or processed content.")
    error: Optional[str] = Field(
        default=None,
        description="Error message if something went wrong; otherwise None.",
    )

class MyToolConfig(BaseToolConfig):
    base_url: str
    timeout: int = 10

class MyTool(BaseTool[MyToolInputSchema, MyToolOutputSchema]):
    def run(self, input: MyToolInputSchema) -> MyToolOutputSchema:
        # Implement pure, side-effect-limited logic here
        try:
            # Example placeholder, to be replaced with real logic:
            content = f"Fetched content from {input.url}"
            return MyToolOutputSchema(content=content)
        except Exception as exc:  # Replace with more specific exceptions in real code
            return MyToolOutputSchema(
                content="",
                error=str(exc),
            )
```

### Context provider skeleton

```python
from dataclasses import dataclass
from typing import List
from atomic_agents.context import BaseDynamicContextProvider

@dataclass
class Item:
    title: str
    body: str

class ItemsContextProvider(BaseDynamicContextProvider):
    def __init__(self, title: str) -> None:
        super().__init__(title=title)
        self.items: List[Item] = []

    def get_info(self) -> str:
        if not self.items:
            return "No items are currently available."
        parts = []
        for idx, item in enumerate(self.items, start=1):
            parts.append(
                f"Item {idx} — {item.title}\n"
                f"{item.body}\n"
                f"{'-' * 80}"
            )
        return "\n\n".join(parts)
```

## Evaluations and iteration

When maintaining this Skill, the owner should periodically evaluate how well it supports atomic-agents workflows. Use scenarios such as:

1. **New agent creation**

   * Query: “Create a decision agent that decides whether my research pipeline should trigger a new web search, given the latest user question and current context providers.”
   * Expected behavior:

     * Proposes `InputSchema` and `OutputSchema`.
     * Uses `SystemPromptGenerator` with clear `background`, `steps`, and `output_instructions`.
     * Returns a complete agent factory function or class definition with `AtomicAgent` + `AgentConfig`.

2. **Tool integration and schema chaining**

   * Query: “Given this REST API spec, build a tool and an agent that prepares the tool’s input schema and processes its output into a user-facing answer.”
   * Expected behavior:

     * Defines `BaseIOSchema` input/output for the tool.
     * Designs an agent whose output schema matches the tool’s input.
     * Shows orchestration where agent output is passed directly into `tool.run(...)`.

3. **Debugging a broken pipeline**

   * Query: “My deep research pipeline occasionally returns empty answers even though pages are scraped. Here is the orchestration code and my context provider; help debug.”
   * Expected behavior:

     * Inspects schemas, context providers, and prompts.
     * Identifies likely issues (e.g., context too long, schema mismatch, missing field in output).
     * Suggests targeted refactors that preserve Atomic Agents’ modularity.

For each scenario, ensure SKILL.md workflows explicitly support the required behaviors. If a scenario fails in practice, refine:

* The workflows (e.g., stronger emphasis on schema design or prompt alignment).
* The templates (e.g., better default skeletons).
* The debugging/refactoring guidance.

Re-run eval scenarios after changes and keep this Skill free of time-sensitive assumptions (e.g., specific version numbers or transient model identifiers) unless the user explicitly wants them.
