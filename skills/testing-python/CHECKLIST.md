# Test Checklist

Use this checklist before committing new tests.

---

## File Structure

- [ ] Test file is in `tests/` mirroring source structure
- [ ] Test file named `test_<module>.py`
- [ ] Imports are organized (stdlib, third-party, local)

---

## Test Organization

- [ ] Each test function tests ONE behavior
- [ ] Test names are descriptive: `test_<describes_behavior>`
- [ ] Related tests are grouped in classes (optional but recommended)
- [ ] No duplicate test coverage

---

## Test Quality

- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] No real API calls, database queries, or network requests
- [ ] External dependencies are mocked
- [ ] Tests are isolated (no shared mutable state)
- [ ] Tests can run in any order

---

## Edge Cases

For each input type, verify coverage:

### Lists
- [ ] Empty list `[]`
- [ ] Single item `[x]`
- [ ] Multiple items `[x, y, z]`
- [ ] Nested lists (if applicable)
- [ ] Lists with None values (if applicable)

### Dicts
- [ ] Empty dict `{}`
- [ ] Missing optional keys
- [ ] Missing required keys (error case)
- [ ] Nested dicts (if applicable)

### Floats
- [ ] Zero `0.0`
- [ ] Negative values
- [ ] `float('nan')` (if applicable)
- [ ] `float('inf')` (if applicable)
- [ ] Very small/large values (if applicable)

### Strings
- [ ] Empty string `""`
- [ ] Whitespace only (if applicable)
- [ ] Unicode characters (if applicable)

### Optional Values
- [ ] `None` input
- [ ] Valid input

---

## Parameterization

- [ ] Same behavior across types → parameterized test
- [ ] Type-specific edge cases → separate tests
- [ ] Error cases with same exception → parameterized
- [ ] Complex setup per case → separate tests

---

## Mocking

- [ ] Mocks are scoped to the test (not global)
- [ ] Mock paths are correct (where it's used, not defined)
- [ ] Return values and side effects are realistic
- [ ] Assertions verify mock interactions when relevant

---

## Fixtures

- [ ] Fixtures have descriptive names
- [ ] Fixtures are in appropriate scope
- [ ] Shared fixtures are in `conftest.py`
- [ ] Factory fixtures used for complex object creation

---

## Execution

- [ ] Tests pass individually: `pytest path/to/test_file.py::test_name`
- [ ] Tests pass as a group: `pytest path/to/test_file.py`
- [ ] No warnings or deprecation notices
- [ ] Tests run quickly (< 1 second per test ideally)

---

## Quick Commands

```bash
# Run single test
pixi run -e dev pytest tests/path/test_file.py::test_name -v

# Run test file
pixi run -e dev pytest tests/path/test_file.py -v

# Run with output
pixi run -e dev pytest tests/path/test_file.py -v -s

# Run and stop on first failure
pixi run -e dev pytest tests/path/test_file.py -x

# Run tests matching pattern
pixi run -e dev pytest tests/ -k "test_empty" -v
```
