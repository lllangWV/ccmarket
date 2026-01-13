````markdown
---
name: using-deltalake
description: Guides an agent to create, read, write, and maintain Delta Lake tables using the delta-rs Python package (`deltalake`) and Arrow-native dataframes. Use when the user needs Delta Lake operations without Spark (local or object storage), including create/append/overwrite, querying with partition pruning, and basic maintenance (vacuum/delete/time travel).
---

# Using `deltalake` (delta-rs) Skill

## Overview

This Skill provides a practical, minimal playbook for working with Delta Lake tables via **delta-rs**’ Python bindings (`deltalake`), centered on:

- **Create / append / overwrite** via `write_deltalake` :contentReference[oaicite:0]{index=0}
- **Read / query** via `DeltaTable` (including partition filters, column selection, and Arrow datasets) :contentReference[oaicite:1]{index=1}
- **Maintenance** (vacuum) and basic DML-style ops (e.g., delete) :contentReference[oaicite:2]{index=2}
- **Cloud object storage configuration**, especially S3 (`storage_options`, locking) :contentReference[oaicite:3]{index=3}

## When to use this Skill

Use this Skill when the user asks to:

- “Create a Delta table from pandas/Polars”
- “Append or overwrite a Delta table” (optionally with schema evolution)
- “Read/query a Delta table into pandas/pyarrow” (preferably filtered)
- “Vacuum a Delta table” / “clean up old files”
- “Use Delta Lake on S3” and pass credentials / configure safe concurrent writes

Do not use this Skill when the user explicitly needs Spark/Databricks-specific APIs (e.g., `spark.read.format("delta")`) unless they still want a delta-rs-based equivalent.

## Environment assumptions & constraints

- Python package: `deltalake` (delta-rs bindings).
- Data inputs commonly: **pandas DataFrame**, **PyArrow Table**, or **PyArrow RecordBatch iterator**. :contentReference[oaicite:4]{index=4}
- Cloud storage access often requires explicit `storage_options` (not “whatever boto3 would do”). :contentReference[oaicite:5]{index=5}

---

# Core workflows

## 1) Create a Delta table

### pandas → Delta
```python
from deltalake import write_deltalake
import pandas as pd

df = pd.DataFrame({"num": [1, 2, 3], "letter": ["a", "b", "c"]})
write_deltalake("tmp/some-table", df)
````

([Delta IO][1])

### Polars → Delta

```python
import polars as pl

df = pl.DataFrame({"num": [1, 2, 3], "letter": ["a", "b", "c"]})
df.write_delta("tmp/some-table")
```

([Delta IO][1])

Operational rule: `write_deltalake` will **create** the table if it does not exist. ([Delta IO][2])

---

## 2) Append vs overwrite (and schema evolution)

### Choose the write mode

* Default behavior is “create-new and error if exists”; control this with `mode`. ([Delta IO][2])
* Use:

  * `mode="append"` to add new data
  * `mode="overwrite"` to replace existing data ([Delta IO][2])

```python
write_deltalake("path/to/table", df, mode="append")
write_deltalake("path/to/table", df, mode="overwrite")
```

([Delta IO][2])

### Handle schema mismatches explicitly

By default, `write_deltalake` raises `ValueError` if incoming schema differs from the table schema. ([Delta IO][2])

If you intend schema evolution:

* `schema_mode="overwrite"`: replace schema entirely (including dropped columns)
* `schema_mode="merge"`: add new columns; missing columns become null
* `schema_mode="merge"` is supported for append operations as well ([Delta IO][2])

```python
write_deltalake("path/to/table", df, mode="overwrite", schema_mode="overwrite")
write_deltalake("path/to/table", df, mode="append", schema_mode="merge")
```

([Delta IO][2])

---

## 3) Load + inspect a table (including time travel)

### Load latest or a specific version

```python
from deltalake import DeltaTable

dt = DeltaTable("path/to/table")           # latest
dt_v3 = DeltaTable("path/to/table", version=3)  # time travel
```

([Delta IO][3])

Useful inspection:

```python
dt.version()
dt.files()
```

([Delta IO][4])

Performance note: for some append-only patterns, you can load without file tracking for lower memory:

```python
dt = DeltaTable("path/to/table", without_files=True)
```

([Delta IO][3])

---

## 4) Query/read efficiently (avoid “load everything”)

### Partition pruning + column projection (recommended default)

```python
from deltalake import DeltaTable

dt = DeltaTable("path/to/partitioned-table")

# Only read year=2021 partition, only "value" column
pdf = dt.to_pandas(partitions=[("year", "=", "2021")], columns=["value"])
```

([Delta IO][5])

Same idea for Arrow:

```python
tbl = dt.to_pyarrow_table(partitions=[("year", "=", "2021")], columns=["value"])
```

([Delta IO][5])

### For non-partition filters or streaming-style reads

Convert to an Arrow Dataset (enables broader filter pushdown + batch processing patterns):

```python
ds = dt.to_pyarrow_dataset()
```

([Delta IO][5])

---

## 5) Maintain the table (vacuum) and basic deletes

### Vacuum (dry-run first by default)

`DeltaTable.vacuum()` lists candidates by default; pass `dry_run=False` to actually delete. Vacuum retains a window (default one week), which impacts time travel. ([Delta IO][6])

```python
dt = DeltaTable("path/to/table")
files_to_delete = dt.vacuum()            # dry-run
dt.vacuum(dry_run=False)                 # executes deletion (be careful)
```

([Delta IO][6])

### Delete rows (predicate as SQL WHERE clause)

```python
dt.delete("some_col = 'bad_value'")
```

If no predicate is provided, it deletes all rows. ([Delta IO][3])

---

# Object storage workflow (AWS S3)

## 1) Credentials: don’t assume boto3 behavior

The delta-rs writer does **not** use boto3 and therefore does **not** automatically read credentials from `~/.aws/config` / `~/.aws/creds`. Plan to pass credentials or rely on supported mechanisms (env vars, profiles, EC2 metadata, etc.). ([Delta IO][7])

## 2) Provide `storage_options` (example pattern)

```python
storage_options = {
    "AWS_REGION": "<region>",
    "AWS_ACCESS_KEY_ID": "<key_id>",
    "AWS_SECRET_ACCESS_KEY": "<secret>",
    # for safe concurrent writes:
    "AWS_S3_LOCKING_PROVIDER": "dynamodb",
    "DELTA_DYNAMO_TABLE_NAME": "delta_log",
}
```

([Delta IO][7])

Use it when writing:

```python
df.write_delta("s3://bucket/delta_table", storage_options=storage_options)
```

([Delta IO][7])

## 3) Concurrency safety on S3

Because S3 does not guarantee mutual exclusion, safe concurrent writes require a locking provider; delta-rs uses DynamoDB for that. An unsafe fallback exists via `AWS_S3_ALLOW_UNSAFE_RENAME=true` (use only if you accept the risk). ([Delta IO][7])

---

# Troubleshooting playbook (fast checks)

1. **Schema mismatch (`ValueError`)**

* Decide whether you intended schema evolution.
* If yes: use `schema_mode="merge"` (additive) or `schema_mode="overwrite"` (replace). ([Delta IO][2])

2. **S3 auth/permission issues**

* Ensure you are passing credentials appropriately (or using env/profile/metadata).
* Ensure S3 permissions include object delete (temporary log files may be deleted even on append-like workflows). ([Delta IO][7])

3. **Slow or memory-heavy reads**

* Apply `partitions=[...]` and `columns=[...]` whenever possible. ([Delta IO][5])
* Prefer `to_pyarrow_dataset()` for broader filters and batch-oriented processing. ([Delta IO][5])
* Consider `without_files=True` for append-only workloads where file listing is unnecessary. ([Delta IO][3])

```

If you want, I can also produce a minimal `TEMPLATES.md` with copy/paste “create/write/read/vacuum/S3” snippets in one place, but the SKILL.md above is intentionally self-contained and concise.
::contentReference[oaicite:33]{index=33}
```

[1]: https://delta-io.github.io/delta-rs/usage/create-delta-lake-table/ "Creating a table - Delta Lake Documentation"
[2]: https://delta-io.github.io/delta-rs/usage/writing/ "Writing Delta Tables - Delta Lake Documentation"
[3]: https://delta-io.github.io/delta-rs/api/delta_table/ "DeltaTable - Delta Lake Documentation"
[4]: https://delta-io.github.io/delta-rs/usage/loading-table/?utm_source=chatgpt.com "Loading a table - Delta Lake Documentation"
[5]: https://delta-io.github.io/delta-rs/usage/querying-delta-tables/ "Querying a table - Delta Lake Documentation"
[6]: https://delta-io.github.io/delta-rs/usage/managing-tables/ "Managing a table - Delta Lake Documentation"
[7]: https://delta-io.github.io/delta-rs/integrations/object-storage/s3/ "AWS S3 Storage Backend - Delta Lake Documentation"
