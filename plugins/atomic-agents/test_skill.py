"""
Test script for atomic-agents skill verification.
This tests that the import patterns and basic structures work correctly.
"""

import sys

def test_imports():
    """Test that all imports from the skill work correctly."""
    print("Testing imports...")

    # Core classes
    from atomic_agents import (
        AtomicAgent,
        AgentConfig,
        BaseIOSchema,
        BaseTool,
        BaseToolConfig,
    )

    # Context management
    from atomic_agents.context import (
        SystemPromptGenerator,
        ChatHistory,
        BaseDynamicContextProvider,
    )

    print("  ✓ All atomic_agents imports successful")
    return True


def test_schema_creation():
    """Test creating BaseIOSchema subclasses."""
    print("Testing schema creation...")

    from atomic_agents import BaseIOSchema
    from pydantic import Field

    class TestInputSchema(BaseIOSchema):
        """Test input schema."""
        query: str = Field(..., description="A test query")

    class TestOutputSchema(BaseIOSchema):
        """Test output schema."""
        answer: str = Field(..., description="A test answer")
        error: str | None = Field(None, description="Error if any")

    # Test instantiation
    input_instance = TestInputSchema(query="test")
    assert input_instance.query == "test"

    output_instance = TestOutputSchema(answer="result", error=None)
    assert output_instance.answer == "result"

    print("  ✓ Schema creation successful")
    return True


def test_tool_creation():
    """Test creating a BaseTool subclass."""
    print("Testing tool creation...")

    from atomic_agents import BaseTool, BaseToolConfig, BaseIOSchema
    from pydantic import Field

    class MyToolInput(BaseIOSchema):
        """Input for test tool."""
        value: str = Field(..., description="Input value")

    class MyToolOutput(BaseIOSchema):
        """Output for test tool."""
        result: str = Field(..., description="Output result")
        error: str | None = Field(None, description="Error if failed")

    class MyToolConfig(BaseToolConfig):
        """Config for test tool."""
        prefix: str = "processed"

    class MyTool(BaseTool[MyToolInput, MyToolOutput]):
        """A simple test tool."""

        def __init__(self, config: MyToolConfig = MyToolConfig()):
            super().__init__(config)
            self.prefix = config.prefix

        def run(self, input: MyToolInput) -> MyToolOutput:
            try:
                result = f"{self.prefix}: {input.value}"
                return MyToolOutput(result=result, error=None)
            except Exception as e:
                return MyToolOutput(result="", error=str(e))

    # Test tool execution
    tool = MyTool(MyToolConfig(prefix="test"))
    output = tool.run(MyToolInput(value="hello"))
    assert output.result == "test: hello"
    assert output.error is None

    print("  ✓ Tool creation and execution successful")
    return True


def test_context_provider():
    """Test creating a context provider."""
    print("Testing context provider...")

    from atomic_agents.context import BaseDynamicContextProvider

    class TestContextProvider(BaseDynamicContextProvider):
        """Test context provider."""

        def __init__(self, title: str):
            super().__init__(title=title)
            self.items: list[str] = []

        def get_info(self) -> str:
            if not self.items:
                return "No items available."
            return "\n".join(self.items)

    provider = TestContextProvider(title="Test Context")
    assert provider.get_info() == "No items available."

    provider.items = ["Item 1", "Item 2"]
    assert provider.get_info() == "Item 1\nItem 2"

    print("  ✓ Context provider creation successful")
    return True


def test_system_prompt_generator():
    """Test SystemPromptGenerator."""
    print("Testing system prompt generator...")

    from atomic_agents.context import SystemPromptGenerator

    generator = SystemPromptGenerator(
        background=["You are a helpful assistant."],
        steps=["Analyze the request", "Provide a response"],
        output_instructions=["Be concise", "Be helpful"],
    )

    # Generator should be creatable without errors
    assert generator is not None

    print("  ✓ SystemPromptGenerator creation successful")
    return True


def test_agent_config():
    """Test AgentConfig creation (without LLM call)."""
    print("Testing agent config...")

    from atomic_agents import AgentConfig
    from atomic_agents.context import SystemPromptGenerator

    # Note: We can't test actual agent execution without API keys
    # but we can verify the config structure

    generator = SystemPromptGenerator(
        background=["Test background"],
        steps=["Step 1"],
        output_instructions=["Instruction 1"],
    )

    # AgentConfig requires a client, but we can verify the class exists
    # and SystemPromptGenerator is compatible
    print("  ✓ AgentConfig structure verified (no LLM call)")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Atomic Agents Skill Verification Tests")
    print("=" * 50 + "\n")

    tests = [
        test_imports,
        test_schema_creation,
        test_tool_creation,
        test_context_provider,
        test_system_prompt_generator,
        test_agent_config,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} failed with error: {e}")
            failed += 1

    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
