# DATA ENGINEERING BEST PRACTICES SKILL

## Purpose
Guide for designing, building, and maintaining production data pipelines with clean, testable, idempotent code.

---

## 1. CORE PRINCIPLES

### Idempotency (Critical)
**Definition:** Running a pipeline multiple times with the same input produces the same output—no duplicates, no stale data.

**Implementation Pattern (Delete-Write):**
```python
# Before writing, remove existing data for the same run_id
if os.path.exists(output_path):
    shutil.rmtree(output_path)
df.to_parquet(output_path, partition_cols=["partition_key"])
```

**SQL Pattern:**
```sql
DELETE FROM final_table WHERE day = 'yyyy-mm-dd';
INSERT INTO final_table SELECT * FROM temp_table;
```

**Requirements:** Replayable source + Overwritable sink

### Functional Programming for Transformations
| Principle | Description | Implementation |
|-----------|-------------|----------------|
| Atomicity | One function = one task | Split multi-purpose functions |
| Idempotency | Same input → same output | Use UPSERT, avoid side effects |
| No Side Effects | Don't modify external state | Accept dependencies as inputs |

```python
# Good: Dependency injection, single responsibility
def load(data, db_conn) -> None:
    cur = db_conn.cursor()
    for record in data:
        cur.execute("INSERT OR REPLACE INTO table VALUES (:id, :value)", record)
```

---

## 2. DATA ARCHITECTURE

### Medallion Architecture (Bronze → Silver → Gold)

| Layer | Purpose | Operations | Users |
|-------|---------|------------|-------|
| **Bronze** | Raw ingestion | Minimal validation, store as string/VARIANT | Data engineers, audit |
| **Silver** | Cleaned data | Schema enforcement, deduplication, null handling, joins | Analysts, data scientists |
| **Gold** | Business-ready | Aggregations, dimensional modeling, KPIs | BI, executives, ML |

**Key Rules:**
- Never write directly to Silver from ingestion—always go through Bronze
- Bronze preserves raw state for reprocessing and audit
- Gold optimized for query performance, not storage efficiency

### Staging Area
**Purpose:** Historical snapshot of source data, enables backfills and data lineage.

**Why Required:**
- Source systems (OLTP) only have current state
- Enables reprocessing with corrected logic
- Provides data lineage for debugging
- Handles schema evolution with date-based logic

---

## 3. EXTRACTION PATTERNS

| Pattern | When to Use | Pros | Cons |
|---------|-------------|------|------|
| **Time-Ranged** | Incremental loads, large datasets | Fast, parallelizable | Complex merge logic, requires replayable source |
| **Full Snapshot** | Dimensional data, small tables | Simple, tracks history | Slow, high storage cost |
| **Lookback** | Rolling metrics (MAU, 30-day KPIs) | Simple for current-state metrics | Metrics may shift with late-arriving data |
| **Streaming** | Real-time needs (fraud detection) | Low latency | Complex (backpressure, checkpointing, exactly-once) |

### Source/Sink Properties

**Replayable Sources:** Event streams, CDC logs, raw dumps  
**Non-Replayable:** Live application tables, APIs returning current state only

**Overwritable Sinks:** Tables with unique keys, namespaced cloud storage  
**Non-Overwritable:** Kafka (no compaction), append-only tables

---

## 4. CODE DESIGN PATTERNS

### Factory Pattern
**Use When:** Multiple similar pipelines (Reddit ETL, Twitter ETL, etc.)

```python
class SocialETL(ABC):
    @abstractmethod
    def extract(self, id, num_records, client): pass
    @abstractmethod
    def transform(self, data): pass
    @abstractmethod
    def load(self, data, db_conn): pass

def etl_factory(source: str) -> tuple[Client, SocialETL]:
    factory = {
        'Reddit': (reddit_client, RedditETL()),
        'Twitter': (twitter_client, TwitterETL()),
    }
    return factory[source]
```

**Don't Use:** When pipelines are fundamentally different, or only 1-2 pipelines exist.

### Strategy Pattern
**Use When:** Multiple interchangeable algorithms for same operation.

```python
def transformation_factory(strategy: str) -> Callable:
    return {
        'sd': standard_deviation_filter,
        'rand': random_choice_filter,
        'none': lambda x: x,
    }[strategy]

# Usage: transform_fn = transformation_factory('sd')
```

### When to Use OOP vs Functions

| Use Functions | Use Classes |
|---------------|-------------|
| Data transformations | External connections (DB, API) |
| Stateless operations | State tracking (logging, metrics) |
| Testable, atomic logic | Configuration management |
| | Pipeline templates |

```python
# OOP for connections
class WarehouseConnection:
    @contextmanager
    def managed_cursor(self):
        conn = psycopg2.connect(self.conn_url)
        cur = conn.cursor()
        try:
            yield cur
        finally:
            conn.commit()
            cur.close()
            conn.close()

# Functions for transforms
def get_monthly_sales(orders: pl.DataFrame) -> pl.DataFrame:
    return orders.group_by("month").agg(pl.col("sales").sum())
```

---

## 5. TESTING STRATEGY

### Implementation Order (Start Broad → Go Narrow)
1. **End-to-End System Tests** — Run full pipeline with sample data, compare output
2. **Data Quality Tests** — Run as pipeline tasks before final load
3. **Monitoring & Alerting** — Track row counts, detect skews
4. **Unit & Contract Tests** — Test individual functions

### Data Quality Checks (Run in Pipeline)
```
Extract → Transform → [Stage to Temp Table] → [Validate] → Load to Final
```

**Validations:** Uniqueness, null checks, allowed values, outlier detection, business rules

### Monitoring Metrics
```json
{
  "run_id": "unique_id",
  "transformation_id": "step_1",
  "row_count_before": 1000,
  "row_count_after": 700,
  "start_datetime": "2024-01-15 04:55:55"
}
```

Set alerts on row count outliers and pipeline failures.

---

## 6. PYTHON ESSENTIALS

### Type Hints
```python
from typing import List, Callable

def extract(id: str, num_records: int) -> List[dict]: ...

def get_transform_fn(name: str) -> Callable[[List[dict]], List[dict]]: ...
```

### Dataclasses
```python
@dataclass
class SocialPost:
    id: str
    title: str
    score: int
    created: datetime
```

### Context Managers (Connection Safety)
```python
@contextmanager
def managed_cursor(self):
    conn = sqlite3.connect(self.db_file)
    cur = conn.cursor()
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()
```

---

## 7. DECISION FRAMEWORK

### Choosing Pipeline Design

```
Is source replayable? 
  NO → Create staging area first, then proceed
  YES ↓

Need historical data in output?
  YES → Full Snapshot or Time-Ranged with history
  NO ↓

Data size?
  LARGE → Time-Ranged or Lookback
  SMALL → Full Snapshot

Real-time requirement?
  YES → Streaming
  NO → Batch (Time-Ranged/Snapshot/Lookback)

Multiple similar pipelines?
  YES → Factory pattern
  NO → Simple functions
```

### Self-Healing Pipelines
When idempotency is hard to maintain:
- Next run catches up failed runs automatically
- Skip failed runs for full-snapshot/lookback pipelines
- Requires metadata tracking of run status

---

## 8. ANTI-PATTERNS TO AVOID

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Singleton for DB connections | Hard to test | Factory pattern |
| No staging area | Can't backfill or audit | Always stage raw data |
| Complex conditional flows | Hard to debug/test | Separate pipelines or strategy pattern |
| Disconnected pipelines | No lineage, SLA issues | Use sensors or unified orchestration |
| Premature abstraction | Slows development | Add patterns only when needed |
| Transformations in classes | Hard to test | Keep transforms as pure functions |

---

## 9. QUICK REFERENCE

**Idempotent Pipeline Checklist:**
- [ ] Replayable source (or staging area)
- [ ] Overwritable sink (unique keys or namespaced storage)
- [ ] Delete-write or UPSERT pattern
- [ ] Run_id-based partitioning

**Code Quality Checklist:**
- [ ] Type hints on all functions
- [ ] Dataclasses for structured data
- [ ] Context managers for connections
- [ ] Tests: system → data quality → unit
- [ ] Logging with row counts per steph