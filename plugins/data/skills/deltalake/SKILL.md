---
name: deltalake
description: Use when working with Delta Lake tables via delta-rs Python bindings (deltalake package). Triggers include creating/appending Delta tables from pandas/polars, querying with partition filters, schema evolution, vacuum, and S3 storage configuration.
---

# Delta Lake with delta-rs

## Overview

The `deltalake` Python package provides Rust-based Delta Lake operations without Spark. Key distinction: this is **not** Spark's `delta` package - do not use `spark.read.format("delta")`.

## Quick Reference

| Operation | Function/Method |
|-----------|-----------------|
| Write table | `write_deltalake(path, df)` |
| Append data | `write_deltalake(path, df, mode="append")` |
| Overwrite | `write_deltalake(path, df, mode="overwrite")` |
| Load table | `DeltaTable(path)` |
| Time travel | `DeltaTable(path, version=N)` |
| Query to pandas | `dt.to_pandas(partitions=[...], columns=[...])` |
| Vacuum | `dt.vacuum(dry_run=False)` |

## Writing Data

```python
from deltalake import write_deltalake
import pandas as pd

df = pd.DataFrame({"id": [1, 2], "value": [10, 20]})

# Create new table
write_deltalake("path/to/table", df)

# Append to existing
write_deltalake("path/to/table", df, mode="append")

# Overwrite existing
write_deltalake("path/to/table", df, mode="overwrite")
```

### With Polars

```python
import polars as pl
df = pl.DataFrame({"id": [1, 2], "value": [10, 20]})
df.write_delta("path/to/table")
```

### Partitioned Tables

```python
write_deltalake("path/to/table", df, partition_by=["year", "month"])
```

## Schema Evolution

By default, schema mismatches raise `ValueError`. Use `schema_mode` to handle changes:

```python
# Add new columns (existing rows get nulls)
write_deltalake("path/to/table", df, mode="append", schema_mode="merge")

# Replace schema entirely
write_deltalake("path/to/table", df, mode="overwrite", schema_mode="overwrite")
```

## Querying Data

```python
from deltalake import DeltaTable

dt = DeltaTable("path/to/table")

# Full table to pandas
df = dt.to_pandas()

# Efficient: partition filter + column projection
df = dt.to_pandas(
    partitions=[("year", "=", "2023")],
    columns=["id", "value"]
)

# Same for PyArrow
table = dt.to_pyarrow_table(
    partitions=[("year", "=", "2023")],
    columns=["id", "value"]
)

# For complex filters, use dataset API
ds = dt.to_pyarrow_dataset()
```

## Table Management

### Vacuum (Clean Old Files)

```python
dt = DeltaTable("path/to/table")

# Dry run first (default) - lists files to delete
files = dt.vacuum()

# Actually delete (CAREFUL: affects time travel)
dt.vacuum(dry_run=False)
```

### Optimize (Compact Small Files)

```python
dt.optimize.compact()
dt.optimize.z_order(["column_name"])
```

### Delete Rows

```python
dt.delete("status = 'invalid'")
```

### Time Travel

```python
dt = DeltaTable("path/to/table", version=5)
# Or load specific timestamp
dt.load_with_datetime("2024-01-15T00:00:00Z")
```

## S3 Storage Configuration

Delta-rs does **not** use boto3 - credentials must be passed explicitly.

```python
storage_options = {
    "AWS_REGION": "us-east-1",
    "AWS_ACCESS_KEY_ID": "...",
    "AWS_SECRET_ACCESS_KEY": "...",
    # For concurrent write safety (recommended):
    "AWS_S3_LOCKING_PROVIDER": "dynamodb",
    "DELTA_DYNAMO_TABLE_NAME": "delta_log",
}

write_deltalake("s3://bucket/table", df, storage_options=storage_options)
dt = DeltaTable("s3://bucket/table", storage_options=storage_options)
```

### DynamoDB Lock Table Setup

```bash
aws dynamodb create-table \
  --table-name delta_log \
  --attribute-definitions \
    AttributeName=tablePath,AttributeType=S \
    AttributeName=fileName,AttributeType=S \
  --key-schema \
    AttributeName=tablePath,KeyType=HASH \
    AttributeName=fileName,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

Without locking, set `AWS_S3_ALLOW_UNSAFE_RENAME=true` (only if single-writer).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `spark.read.format("delta")` | Use `DeltaTable(path).to_pandas()` |
| Assuming boto3 credentials work | Pass `storage_options` explicitly |
| Running `vacuum()` without checking | Always dry run first: `dt.vacuum()` |
| Loading full table to filter | Use `partitions=` and `columns=` parameters |
| Schema mismatch error on append | Add `schema_mode="merge"` |
