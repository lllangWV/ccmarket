---
name: python-typing
description: Use when asking about Python type hints, type checking errors, creating type stubs, fixing pyright/mypy errors, or needing guidance on TypeVar, Protocol, TypedDict, overloads, invariance, or type narrowing
---

# Python Typing Best Practices

Quick reference for fixing type errors and writing correct type annotations.

## Common Errors → Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `list[X] not assignable to list[X\|Y]` | Invariant container | Use `Sequence[X\|Y]` or `Iterable[X\|Y]` |
| `"T \| None" has no attribute` | Missing null check | Add guard: `if x is None: raise/return` |
| Missing type annotation | Untyped parameter/return | Add annotation; use `TypeVar` for generics |
| `Unknown` type | Inference failed | Add explicit annotation |
| `reportMissingTypeStubs` | No stubs for library | Search PyPI for `types-<pkg>` or `<pkg>-stubs`, or create custom stubs |

## Type Constructs

| Need | Use | Example |
|------|-----|---------|
| Preserve caller's type | `TypeVar` | `T = TypeVar("T")` |
| Accept any with method X | `Protocol` | `class Readable(Protocol): def read(self) -> str: ...` |
| Dict with fixed keys | `TypedDict` | `class Config(TypedDict): host: str; port: int` |
| Return depends on arg | `@overload` | Multiple signatures |
| Narrow in both branches | `TypeIs` | `def is_str(x: object) -> TypeIs[str]` |

## Invariance

Mutable containers (`list`, `dict`, `set`) are **invariant**:

```python
# ❌ list[int] NOT assignable to list[int | None]
def process(items: list[int | None]) -> int: ...
nums: list[int] = [1, 2, 3]
process(nums)  # Error!

# ✅ Use read-only type (covariant)
def process(items: Sequence[int | None]) -> int: ...
process(nums)  # OK
```

**Rule:** If function only reads, use `Sequence`, `Mapping`, or `Iterable`.

## Type Narrowing

Narrow `T | None` before accessing attributes:

```python
# ❌ No narrowing
def get_domain(email: str | None) -> str:
    return email.split("@")[1]  # Error

# ✅ Guard narrows type
def get_domain(email: str | None) -> str:
    if email is None:
        raise ValueError("email required")
    return email.split("@")[1]  # OK - narrowed to str
```

**Narrowing constructs:** `if x is None`, `isinstance()`, `assert`, `TypeIs`

## Generics with TypeVar

```python
from typing import TypeVar

T = TypeVar("T")

def first_or_default(items: list[T], default: T) -> T:
    return items[0] if items else default

# Caller gets precise type
x: int = first_or_default([1, 2], 0)  # T=int
```

**`Any` vs `TypeVar`:** `Any` disables checking. `TypeVar` preserves it.

## Protocols

For "anything with method X" without inheritance:

```python
from typing import Protocol

class Readable(Protocol):
    def read(self) -> str: ...

def read_all(r: Readable) -> str:
    return r.read()

# Works with any class having read() -> str
read_all(open("file.txt"))
read_all(io.StringIO("data"))
```

## Overloads

When return type depends on argument:

```python
from typing import overload

@overload
def get(key: str, default: None = None) -> str | None: ...
@overload
def get(key: str, default: str) -> str: ...

def get(key: str, default: str | None = None) -> str | None:
    return data.get(key, default)
```

## TypedDict

For dicts with known structure:

```python
from typing import TypedDict, NotRequired

class Response(TypedDict):
    status: str
    data: dict[str, object]
    error: NotRequired[str]  # Optional key
```

## Creating Type Stubs

When `reportMissingTypeStubs` errors appear and no package exists:

### 1. Search First
- `types-<package>` (typeshed convention)
- `<package>-stubs` (alternative)

### 2. Generate with stubgen
```bash
stubgen -p pkg -o stubs/ --inspect-mode
```

### 3. Configure pyright/mypy
```toml
[tool.pyright]
stubPath = "stubs"

[tool.mypy]
mypy_path = "stubs"
```

### 4. Stub Syntax
```python
from _typeshed import Incomplete

class Thing:
    name: str
    _internal: Incomplete  # Unknown type (NOT Any)
    def __init__(self, x: int | None = ...) -> None: ...

# Partial class - add __getattr__
class PartiallyTyped:
    known_attr: str
    def __getattr__(self, name: str) -> Incomplete: ...
```

### 5. Verify
```bash
python -m mypy.stubtest pkg
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `Any` for unknown types | Use `Incomplete` in stubs |
| Implementation signature after overloads | Only `@overload` variants in stubs |
| Missing `-> None` on `__init__` | Always annotate |
| `Union[X, Y]` syntax | Use `X \| Y` |
| `typing.List`, `typing.Dict` | Use `list`, `dict` builtins |
| `typing.Mapping` | Use `collections.abc.Mapping` |
| Using `dict` for read-only params | Use `Mapping` (covariant) |
