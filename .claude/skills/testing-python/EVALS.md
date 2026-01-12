# Evaluation Scenarios

Use these scenarios to verify the testing-python skill produces correct test code.

---

## Scenario 1: Basic Function Testing

**Query:** "Write tests for this function"

**Input Code:**
```python
# src/researchboi/utils/math.py
def add_numbers(a: int, b: int) -> int:
    return a + b
```

**Expected Behavior:**
- Creates `tests/utils/test_math.py`
- Tests basic addition
- Tests edge cases (zero, negative)
- Uses descriptive test names

**Example Expected Output:**
```python
# tests/utils/test_math.py
def test_adds_two_positive_numbers():
    assert add_numbers(2, 3) == 5

def test_adds_zero():
    assert add_numbers(5, 0) == 5

def test_adds_negative_numbers():
    assert add_numbers(-2, -3) == -5
```

---

## Scenario 2: Function with Multiple Input Types

**Query:** "Write tests for this function that accepts different types"

**Input Code:**
```python
# src/researchboi/utils/processor.py
def get_length(data):
    """Return length of data. Works with str, list, dict."""
    return len(data)
```

**Expected Behavior:**
- Uses parameterized test for same behavior
- Covers edge cases per type (empty values)
- Separate tests if needed for type-specific behavior

**Example Expected Output:**
```python
@pytest.mark.parametrize("input_val,expected", [
    ("hello", 5),
    ([1, 2, 3], 3),
    ({"a": 1, "b": 2}, 2),
])
def test_returns_length_for_various_types(input_val, expected):
    assert get_length(input_val) == expected

@pytest.mark.parametrize("empty_val", ["", [], {}])
def test_returns_zero_for_empty_values(empty_val):
    assert get_length(empty_val) == 0
```

---

## Scenario 3: Class with External Dependency

**Query:** "Write tests for this service that calls an API"

**Input Code:**
```python
# src/researchboi/services/weather.py
import requests

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.weather.com"

    def get_temperature(self, city: str) -> float:
        response = requests.get(
            f"{self.base_url}/current",
            params={"city": city, "key": self.api_key}
        )
        response.raise_for_status()
        return response.json()["temperature"]
```

**Expected Behavior:**
- Mocks `requests.get` - NO real API calls
- Tests successful response
- Tests error handling (404, network error)
- Uses descriptive test names

**Example Expected Output:**
```python
from unittest.mock import patch, Mock
import pytest

class TestWeatherService:
    @patch("researchboi.services.weather.requests.get")
    def test_returns_temperature_from_api(self, mock_get):
        mock_get.return_value.json.return_value = {"temperature": 72.5}
        mock_get.return_value.raise_for_status = Mock()

        service = WeatherService(api_key="test-key")
        result = service.get_temperature("NYC")

        assert result == 72.5

    @patch("researchboi.services.weather.requests.get")
    def test_raises_for_invalid_city(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = requests.HTTPError()

        service = WeatherService(api_key="test-key")

        with pytest.raises(requests.HTTPError):
            service.get_temperature("InvalidCity")
```

---

## Scenario 4: Function with Complex Edge Cases

**Query:** "Write tests for this validator"

**Input Code:**
```python
# src/researchboi/validators/config.py
def validate_config(config: dict) -> dict:
    """Validate and normalize config dict.

    Required keys: name, version
    Optional keys: debug (default False), timeout (default 30)
    """
    if not isinstance(config, dict):
        raise TypeError("Config must be a dict")

    if "name" not in config:
        raise ValueError("Config must have 'name'")
    if "version" not in config:
        raise ValueError("Config must have 'version'")

    return {
        "name": config["name"],
        "version": config["version"],
        "debug": config.get("debug", False),
        "timeout": config.get("timeout", 30),
    }
```

**Expected Behavior:**
- Tests valid config
- Tests missing required keys (separate tests)
- Tests default values for optional keys
- Tests type error
- Uses descriptive names

**Example Expected Output:**
```python
class TestValidateConfig:
    def test_returns_normalized_config_with_all_keys(self):
        config = {"name": "app", "version": "1.0", "debug": True, "timeout": 60}
        result = validate_config(config)
        assert result == {"name": "app", "version": "1.0", "debug": True, "timeout": 60}

    def test_applies_default_debug_false(self):
        config = {"name": "app", "version": "1.0"}
        result = validate_config(config)
        assert result["debug"] is False

    def test_applies_default_timeout_30(self):
        config = {"name": "app", "version": "1.0"}
        result = validate_config(config)
        assert result["timeout"] == 30

    def test_raises_value_error_when_name_missing(self):
        with pytest.raises(ValueError, match="must have 'name'"):
            validate_config({"version": "1.0"})

    def test_raises_value_error_when_version_missing(self):
        with pytest.raises(ValueError, match="must have 'version'"):
            validate_config({"name": "app"})

    def test_raises_type_error_for_non_dict(self):
        with pytest.raises(TypeError, match="must be a dict"):
            validate_config("not a dict")
```

---

## Scenario 5: Using Fixtures

**Query:** "Write tests using fixtures for this file processor"

**Input Code:**
```python
# src/researchboi/io/reader.py
from pathlib import Path

def read_lines(filepath: Path) -> list[str]:
    """Read file and return non-empty lines."""
    with open(filepath) as f:
        return [line.strip() for line in f if line.strip()]
```

**Expected Behavior:**
- Uses `tmp_path` fixture for temp files
- Tests empty file
- Tests file with content
- Tests file with blank lines

**Example Expected Output:**
```python
import pytest
from pathlib import Path

class TestReadLines:
    def test_returns_empty_list_for_empty_file(self, tmp_path):
        file = tmp_path / "empty.txt"
        file.write_text("")

        result = read_lines(file)

        assert result == []

    def test_returns_lines_from_file(self, tmp_path):
        file = tmp_path / "data.txt"
        file.write_text("line1\nline2\nline3\n")

        result = read_lines(file)

        assert result == ["line1", "line2", "line3"]

    def test_skips_blank_lines(self, tmp_path):
        file = tmp_path / "data.txt"
        file.write_text("line1\n\n\nline2\n")

        result = read_lines(file)

        assert result == ["line1", "line2"]
```

---

## Evaluation Rubric

| Criterion | Pass | Fail |
|-----------|------|------|
| Correct file location | `tests/` mirrors source | Wrong directory |
| Naming convention | `test_<describes_behavior>` | Vague names like `test_1` |
| One behavior per test | Single assert per behavior | Multiple unrelated asserts |
| External calls mocked | No real API/DB calls | Real network requests |
| Edge cases covered | Empty, None, boundaries | Only happy path |
| Parameterization | Used when same behavior | Over/under parameterized |
| Fixtures | Used for setup | Repeated setup code |
