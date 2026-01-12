# Test Templates

## Basic Test File Template

```python
"""Tests for <module_name>."""

import pytest
from unittest.mock import Mock, patch

from researchboi.<path>.<module> import <ClassOrFunction>


class Test<ClassName>:
    """Tests for <ClassName>."""

    def test_<behavior_description>(self):
        """<Brief description of what is being tested>."""
        # Arrange
        instance = <ClassName>()

        # Act
        result = instance.<method>()

        # Assert
        assert result == expected_value

    def test_<another_behavior>(self):
        """<Brief description>."""
        # Arrange
        # Act
        # Assert
        pass
```

---

## Parameterized Test Template

### Same Behavior Across Types

```python
import pytest

@pytest.mark.parametrize("input_val,expected", [
    ([1, 2, 3], 6),           # list
    ((1, 2, 3), 6),           # tuple
    ({1, 2, 3}, 6),           # set
])
def test_sum_accepts_iterables(input_val, expected):
    """Verify sum works with different iterable types."""
    assert sum_values(input_val) == expected
```

### Testing Multiple Valid Inputs

```python
@pytest.mark.parametrize("valid_input", [
    "hello",
    "world",
    "test123",
    "with-hyphen",
    "with_underscore",
])
def test_accepts_valid_strings(valid_input):
    """Verify function accepts various valid string formats."""
    result = validate_name(valid_input)
    assert result is True
```

### Testing Multiple Error Cases

```python
@pytest.mark.parametrize("invalid_input,error_msg", [
    ("", "Name cannot be empty"),
    ("ab", "Name must be at least 3 characters"),
    ("a" * 101, "Name cannot exceed 100 characters"),
    ("has spaces", "Name cannot contain spaces"),
])
def test_rejects_invalid_names(invalid_input, error_msg):
    """Verify appropriate error messages for invalid inputs."""
    with pytest.raises(ValueError, match=error_msg):
        validate_name(invalid_input)
```

### With IDs for Better Output

```python
@pytest.mark.parametrize("input_val,expected", [
    pytest.param([], 0, id="empty_list"),
    pytest.param([1], 1, id="single_item"),
    pytest.param([1, 2, 3], 6, id="multiple_items"),
])
def test_sum_list(input_val, expected):
    assert sum_values(input_val) == expected
```

---

## Fixture Templates

### Simple Data Fixture

```python
@pytest.fixture
def sample_user():
    """Provide a sample user dict for testing."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }
```

### Factory Fixture

```python
@pytest.fixture
def make_user():
    """Factory fixture to create users with custom attributes."""
    def _make_user(name="Test", email=None, **kwargs):
        return {
            "name": name,
            "email": email or f"{name.lower()}@example.com",
            **kwargs,
        }
    return _make_user

def test_user_factory(make_user):
    user1 = make_user(name="Alice")
    user2 = make_user(name="Bob", role="admin")

    assert user1["email"] == "alice@example.com"
    assert user2["role"] == "admin"
```

### Setup/Teardown Fixture

```python
@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary config file, clean up after test."""
    config_path = tmp_path / "config.yaml"
    config_path.write_text("key: value\n")

    yield config_path  # Test runs here

    # Teardown: tmp_path is auto-cleaned by pytest
```

### Mock Fixture

```python
@pytest.fixture
def mock_api_client():
    """Provide a pre-configured mock API client."""
    client = Mock()
    client.get.return_value = {"status": "ok", "data": []}
    client.post.return_value = {"status": "created", "id": 1}
    return client
```

---

## Mocking Templates

### Patch as Decorator

```python
@patch("researchboi.services.api.requests.get")
def test_fetches_data(mock_get):
    mock_get.return_value.json.return_value = {"items": [1, 2, 3]}
    mock_get.return_value.status_code = 200

    service = ApiService()
    result = service.fetch_items()

    assert len(result) == 3
    mock_get.assert_called_once_with("https://api.example.com/items")
```

### Patch as Context Manager

```python
def test_handles_timeout():
    with patch("researchboi.services.api.requests.get") as mock_get:
        mock_get.side_effect = Timeout("Connection timed out")

        service = ApiService()
        result = service.fetch_safe()

        assert result is None
```

### Patch Multiple Objects

```python
@patch("researchboi.services.api.requests.post")
@patch("researchboi.services.api.requests.get")
def test_workflow(mock_get, mock_post):  # Note: reverse order
    mock_get.return_value.json.return_value = {"id": 1}
    mock_post.return_value.status_code = 201

    # Test code here
```

### Patch Object Attribute

```python
def test_with_custom_timeout():
    service = ApiService()

    with patch.object(service, "timeout", 5):
        assert service.timeout == 5
```

---

## Exception Testing Templates

### Basic Exception Test

```python
def test_raises_value_error_for_negative():
    with pytest.raises(ValueError):
        calculate_sqrt(-1)
```

### With Message Matching

```python
def test_raises_with_message():
    with pytest.raises(ValueError, match="must be positive"):
        calculate_sqrt(-1)
```

### Capturing Exception Info

```python
def test_exception_details():
    with pytest.raises(ValidationError) as exc_info:
        validate_config({"invalid": "config"})

    assert "missing required field" in str(exc_info.value)
    assert exc_info.value.field == "name"
```

---

## Async Test Template

```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch():
    service = AsyncService()
    result = await service.fetch_data()
    assert result is not None
```

---

## conftest.py Template

```python
"""Shared fixtures for tests."""

import pytest
from unittest.mock import Mock


# ============================================================
# Data Fixtures
# ============================================================

@pytest.fixture
def sample_config():
    """Standard configuration for testing."""
    return {
        "timeout": 30,
        "retries": 3,
        "debug": False,
    }


# ============================================================
# Mock Fixtures
# ============================================================

@pytest.fixture
def mock_http_client():
    """Mock HTTP client for API tests."""
    client = Mock()
    client.get.return_value.status_code = 200
    client.get.return_value.json.return_value = {}
    return client


# ============================================================
# File System Fixtures
# ============================================================

@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace directory."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "input").mkdir()
    (workspace / "output").mkdir()
    return workspace


# ============================================================
# Factory Fixtures
# ============================================================

@pytest.fixture
def make_tool_result():
    """Factory for creating tool results."""
    def _make(success=True, output="", error=None):
        return {
            "success": success,
            "output": output,
            "error": error,
        }
    return _make
```
