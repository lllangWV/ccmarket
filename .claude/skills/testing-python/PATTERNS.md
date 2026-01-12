# Testing Patterns

## Decision: Parameterized vs Separate Tests

### Use Parameterized Tests When

**Same expected behavior across types:**

```python
@pytest.mark.parametrize("input_val,expected", [
    ([1, 2, 3], "list result"),
    ({"a": 1}, "dict result"),
    (3.14, "float result"),
])
def test_process_accepts_various_types(input_val, expected):
    assert process(input_val) == expected
```

**Testing a series of valid inputs:**

```python
@pytest.mark.parametrize("valid_email", [
    "user@example.com",
    "user.name@example.com",
    "user+tag@example.org",
])
def test_accepts_valid_emails(valid_email):
    assert is_valid_email(valid_email) is True
```

**Same error type for different invalid inputs:**

```python
@pytest.mark.parametrize("invalid_input", [
    "",
    None,
    "   ",
])
def test_rejects_empty_values(invalid_input):
    with pytest.raises(ValueError):
        process_name(invalid_input)
```

### Use Separate Tests When

**Type-specific edge cases:**

```python
# List has unique edge cases
def test_handles_empty_list():
    assert process([]) == default_value

def test_handles_nested_list():
    assert process([[1, 2], [3, 4]]) == flattened_result

def test_handles_list_with_none_elements():
    assert process([1, None, 3]) == filtered_result


# Dict has different edge cases
def test_handles_empty_dict():
    assert process({}) == default_value

def test_handles_missing_required_key():
    with pytest.raises(KeyError):
        process({"wrong_key": 1})

def test_handles_nested_dict():
    assert process({"outer": {"inner": 1}}) == nested_result
```

**Complex setup differs per case:**

```python
def test_processes_small_file():
    content = "small content"
    with create_temp_file(content) as f:
        result = process_file(f)
    assert result.size < 1000

def test_processes_large_file_in_chunks():
    content = "x" * 1_000_000
    with create_temp_file(content) as f:
        result = process_file(f)
    assert result.was_chunked is True
```

---

## Edge Cases by Type

### List Edge Cases

```python
class TestListProcessing:
    def test_empty_list(self):
        assert process([]) == []

    def test_single_item_list(self):
        assert process([1]) == [1]

    def test_multiple_items(self):
        assert process([1, 2, 3]) == [1, 2, 3]

    def test_nested_list(self):
        assert process([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    def test_list_with_none_values(self):
        assert process([1, None, 3]) == [1, 3]

    def test_list_with_duplicates(self):
        assert process([1, 1, 2, 2]) == [1, 2]
```

### Dict Edge Cases

```python
class TestDictProcessing:
    def test_empty_dict(self):
        assert process({}) == {}

    def test_single_key(self):
        assert process({"a": 1}) == {"a": 1}

    def test_missing_optional_key(self):
        result = process({"required": 1})
        assert result["optional"] == default_value

    def test_missing_required_key(self):
        with pytest.raises(KeyError, match="required"):
            process({"wrong": 1})

    def test_nested_dict(self):
        input_data = {"outer": {"inner": {"deep": 1}}}
        assert process(input_data)["outer"]["inner"]["deep"] == 1

    def test_dict_with_none_value(self):
        assert process({"key": None}) == {"key": default}
```

### Float Edge Cases

```python
import math

class TestFloatProcessing:
    def test_zero(self):
        assert process(0.0) == 0.0

    def test_negative(self):
        assert process(-1.5) == expected_negative

    def test_very_small(self):
        assert process(1e-10) == expected_small

    def test_very_large(self):
        assert process(1e10) == expected_large

    def test_nan(self):
        result = process(float("nan"))
        assert math.isnan(result)

    def test_positive_infinity(self):
        assert process(float("inf")) == expected_inf

    def test_negative_infinity(self):
        assert process(float("-inf")) == expected_neg_inf
```

### String Edge Cases

```python
class TestStringProcessing:
    def test_empty_string(self):
        assert process("") == ""

    def test_whitespace_only(self):
        assert process("   ") == ""

    def test_unicode(self):
        assert process("Hello, 世界!") == expected_unicode

    def test_special_characters(self):
        assert process("test@#$%") == expected_special

    def test_very_long_string(self):
        long_input = "x" * 10000
        result = process(long_input)
        assert len(result) <= max_length

    def test_newlines_and_tabs(self):
        assert process("line1\nline2\ttab") == expected
```

### Optional/None Edge Cases

```python
class TestOptionalHandling:
    def test_none_input(self):
        assert process(None) == default_value

    def test_valid_input(self):
        assert process("valid") == "valid"

    def test_none_in_optional_field(self):
        data = {"required": 1, "optional": None}
        result = process(data)
        assert result["optional"] == default_value
```

---

## Mocking Patterns

### Mock API Responses

```python
@patch("researchboi.services.client.requests.get")
def test_handles_successful_response(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": [1, 2, 3]}

    result = fetch_data()

    assert result == [1, 2, 3]


@patch("researchboi.services.client.requests.get")
def test_handles_404_response(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"error": "Not found"}

    result = fetch_data()

    assert result is None


@patch("researchboi.services.client.requests.get")
def test_handles_network_error(mock_get):
    mock_get.side_effect = ConnectionError("Network unreachable")

    with pytest.raises(ServiceUnavailableError):
        fetch_data()
```

### Mock File Operations

```python
def test_reads_config_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("key: value\n")

    result = load_config(config_file)

    assert result["key"] == "value"


def test_handles_missing_file(tmp_path):
    missing_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        load_config(missing_file)
```

### Mock External Services

```python
@pytest.fixture
def mock_database():
    db = Mock()
    db.query.return_value = [{"id": 1, "name": "Test"}]
    db.insert.return_value = {"id": 2}
    return db


def test_fetches_from_database(mock_database):
    service = DataService(db=mock_database)

    result = service.get_all()

    assert len(result) == 1
    mock_database.query.assert_called_once()
```

### Mock Time/Date

```python
from unittest.mock import patch
from datetime import datetime

@patch("researchboi.utils.datetime")
def test_uses_current_time(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 15, 10, 30)

    result = generate_timestamp()

    assert result == "2024-01-15T10:30:00"
```

---

## Anti-Patterns to Avoid

### Multiple Assertions Testing Different Behaviors

```python
# Bad - testing multiple behaviors in one test
def test_user_processing():
    user = create_user("test")
    assert user.name == "test"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.created_at is not None

# Good - separate test per behavior
def test_user_has_name():
    user = create_user("test")
    assert user.name == "test"

def test_user_has_default_email():
    user = create_user("test")
    assert user.email == "test@example.com"

def test_user_is_active_by_default():
    user = create_user("test")
    assert user.is_active is True
```

### Testing Implementation Details

```python
# Bad - testing private methods
def test_internal_cache():
    service = DataService()
    service._cache["key"] = "value"
    assert service._cache["key"] == "value"

# Good - testing public behavior
def test_caches_repeated_requests():
    service = DataService()
    result1 = service.fetch("key")
    result2 = service.fetch("key")
    assert result1 == result2
    # Optionally verify only one API call was made
```

### Overly Broad Parameterization

```python
# Bad - mixing unrelated test cases
@pytest.mark.parametrize("input_val,expected", [
    ("valid", True),
    ("", False),
    (None, ValueError),  # Different behavior - raises exception
    ([1, 2], TypeError),  # Different behavior - raises exception
])
def test_validate(input_val, expected):
    # Complex logic to handle both returns and exceptions
    pass

# Good - separate concerns
@pytest.mark.parametrize("valid_input", ["valid", "also_valid"])
def test_accepts_valid_input(valid_input):
    assert validate(valid_input) is True

@pytest.mark.parametrize("invalid_input", ["", "   "])
def test_rejects_empty_input(invalid_input):
    assert validate(invalid_input) is False

@pytest.mark.parametrize("bad_type", [None, [], {}])
def test_raises_for_wrong_type(bad_type):
    with pytest.raises(TypeError):
        validate(bad_type)
```

### Not Isolating Tests

```python
# Bad - tests depend on shared state
class TestCounter:
    counter = Counter()  # Shared instance!

    def test_increment(self):
        self.counter.increment()
        assert self.counter.value == 1

    def test_starts_at_zero(self):
        assert self.counter.value == 0  # Fails if test_increment runs first!

# Good - isolated tests
class TestCounter:
    def test_increment(self):
        counter = Counter()
        counter.increment()
        assert counter.value == 1

    def test_starts_at_zero(self):
        counter = Counter()
        assert counter.value == 0
```
