# Testing Python Code with Pytest

## Purpose

This skill guides writing well-structured pytest unit tests that:
- Test logical units and their boundaries
- Follow behavior-driven conventions (one test = one behavior)
- Use mocks for external dependencies (API calls, databases, file I/O)
- Apply parameterized tests appropriately

---

## When to Use This Skill

Use this skill when the user:
- Asks to "write tests", "add tests", or "create tests" for Python code
- Wants to test a specific module, class, or function
- Asks about testing patterns, fixtures, or mocking
- Needs help structuring test files

**Do NOT use** when:
- User wants integration or end-to-end tests (different patterns apply)
- User is debugging existing tests (use standard debugging)
- User wants performance/load testing

---

## Test File Organization

### Directory Structure

Tests live in `ROOT/tests/` and mirror the source structure:

```
src/researchboi/
├── tools/
│   ├── bash.py
│   └── grep.py
├── agents/
│   └── orchestrator.py
└── schemas/
    └── research.py

tests/
├── tools/
│   ├── test_bash.py
│   └── test_grep.py
├── agents/
│   └── test_orchestrator.py
└── schemas/
    └── test_research.py
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Test file | `test_<module>.py` | `test_bash.py` |
| Test class | `Test<ClassName>` | `TestBashTool` |
| Test function | `test_<behavior_description>` | `test_returns_empty_list_when_input_is_none` |

### Test Function Naming

Names should describe the **behavior being tested**, not the implementation:

```python
# Good - describes behavior
def test_returns_error_when_file_not_found():
def test_parses_nested_dict_correctly():
def test_raises_value_error_for_negative_input():

# Bad - describes implementation
def test_function():
def test_parse():
def test_error():
```

---

## Core Workflow

### 1. Identify the Unit to Test

Before writing tests, identify:
- What is the logical unit? (function, method, class)
- What are its inputs and outputs?
- What are the boundaries? (valid inputs, invalid inputs, edge cases)
- What external dependencies does it have? (APIs, files, databases)

### 2. Create Test File

```bash
# Determine test file path
# Source: src/researchboi/tools/bash.py
# Test:   tests/tools/test_bash.py

mkdir -p tests/tools
touch tests/tools/test_bash.py
```

### 3. Write Tests Following the Pattern

For each behavior:
1. **Arrange** - Set up test data and mocks
2. **Act** - Call the function/method
3. **Assert** - Verify the expected outcome

```python
def test_returns_stdout_when_command_succeeds():
    # Arrange
    tool = BashTool()

    # Act
    result = tool.run("echo hello")

    # Assert
    assert result.stdout == "hello\n"
```

### 4. Decide: Parameterized vs Separate Tests

**Use parameterized tests when:**
- Same behavior across different input types
- Testing a list of valid inputs
- Testing multiple error cases with same error type

**Use separate tests when:**
- Different types have unique edge cases
- Different code paths are exercised
- Complex setup differs per case

See [PATTERNS.md](PATTERNS.md) for detailed guidance.

### 5. Mock External Dependencies

Never make real API calls, database queries, or file system operations in unit tests:

```python
from unittest.mock import Mock, patch

def test_fetches_data_from_api():
    # Mock the API client
    mock_client = Mock()
    mock_client.get.return_value = {"status": "ok"}

    service = DataService(client=mock_client)
    result = service.fetch_data()

    assert result["status"] == "ok"
    mock_client.get.assert_called_once()
```

### 6. Run and Verify

```bash
# Run specific test file
pixi run -e dev pytest tests/tools/test_bash.py -v

# Run specific test
pixi run -e dev pytest tests/tools/test_bash.py::test_returns_stdout_when_command_succeeds -v
```

---

## Fixtures

Use fixtures for reusable setup. Define in `conftest.py` for sharing across tests.

### Local Fixtures (same file)

```python
import pytest

@pytest.fixture
def sample_config():
    return {"timeout": 30, "retries": 3}

def test_uses_timeout_from_config(sample_config):
    processor = Processor(config=sample_config)
    assert processor.timeout == 30
```

### Shared Fixtures (conftest.py)

```python
# tests/conftest.py
import pytest

@pytest.fixture
def mock_api_client():
    from unittest.mock import Mock
    client = Mock()
    client.get.return_value = {"data": []}
    return client

@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace directory."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace
```

### Fixture Scopes

| Scope | When to Use |
|-------|-------------|
| `function` (default) | Fresh instance per test |
| `class` | Shared across test class |
| `module` | Shared across test file |
| `session` | Shared across entire test run |

```python
@pytest.fixture(scope="module")
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()
```

---

## Mocking Patterns

### Patch Decorator

```python
from unittest.mock import patch

@patch("researchboi.tools.bash.subprocess.run")
def test_executes_command(mock_run):
    mock_run.return_value = Mock(stdout="output", returncode=0)

    tool = BashTool()
    result = tool.run("ls")

    mock_run.assert_called_once()
```

### Context Manager

```python
def test_handles_api_error():
    with patch("researchboi.services.api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("Network error")

        service = ApiService()
        result = service.fetch_safe()

        assert result is None
```

### Mock Return Values and Side Effects

```python
# Return different values on successive calls
mock.return_value = "value"
mock.side_effect = [1, 2, 3]  # Returns 1, then 2, then 3
mock.side_effect = ValueError("error")  # Raises exception
```

---

## Edge Cases to Cover

Always test boundaries. See [PATTERNS.md](PATTERNS.md) for type-specific patterns.

| Type | Edge Cases |
|------|------------|
| List | `[]`, `[single]`, `[many, items]`, nested lists |
| Dict | `{}`, missing keys, nested dicts |
| Float | `0.0`, negative, `float('nan')`, `float('inf')`, very small |
| String | `""`, whitespace only, unicode, very long |
| Optional | `None` vs valid value |

---

## References

- [TEMPLATES.md](TEMPLATES.md) - Test file templates and examples
- [PATTERNS.md](PATTERNS.md) - Parameterization and edge case patterns
- [CHECKLIST.md](CHECKLIST.md) - Pre-commit checklist
- [EVALS.md](EVALS.md) - Evaluation scenarios

---

## Quick Reference

```python
# Basic test structure
def test_<describes_behavior>():
    # Arrange
    ...
    # Act
    result = function_under_test(input)
    # Assert
    assert result == expected

# Parameterized test
@pytest.mark.parametrize("input_val,expected", [
    (input1, expected1),
    (input2, expected2),
])
def test_<behavior>(input_val, expected):
    assert function(input_val) == expected

# Mock external call
@patch("module.path.external_function")
def test_<behavior>(mock_func):
    mock_func.return_value = fake_response
    ...

# Fixture usage
@pytest.fixture
def setup_data():
    return {"key": "value"}

def test_uses_fixture(setup_data):
    assert setup_data["key"] == "value"
```
