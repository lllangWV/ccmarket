# Evaluation scenarios (MinerU Skill)

## Eval 1 — Basic markdown + content_list extraction
{
  "skills": ["processing-pdfs-mineru"],
  "query": "Convert this PDF to Markdown and give me the reading-order JSON too.",
  "files": ["test-files/sample.pdf"],
  "expected_behavior": [
    "Chooses a backend and method (pipeline auto by default) and states why",
    "Runs mineru with explicit flags",
    "Produces .md and *_content_list.json (and notes other outputs)",
    "Validates files exist and are non-empty",
    "Returns a short extraction report summarizing outputs and QA"
  ]
}

## Eval 2 — Table export
{
  "skills": ["processing-pdfs-mineru"],
  "query": "Extract all tables into a single tables.html and a tables.json with captions.",
  "files": ["test-files/tables-heavy.pdf"],
  "expected_behavior": [
    "Uses *_content_list.json to locate type==table blocks",
    "Exports HTML tables and includes page_idx/bbox/captions/footnotes",
    "Notes limitations if table_body is missing and offers fallback"
  ]
}

## Eval 3 — Debug missing text / wrong order
{
  "skills": ["processing-pdfs-mineru"],
  "query": "MinerU is missing text on pages 3–5. Diagnose and recommend rerun settings.",
  "files": ["test-files/problem.pdf"],
  "expected_behavior": [
    "Restricts run to pages 3–5 using --start/--end",
    "Checks *_layout.pdf for layout/read-order issues",
    "Checks *_spans.pdf (pipeline) for span-level text loss",
    "Recommends concrete rerun changes (method=ocr, lang=..., toggles, backend switch)",
    "Documents the iteration plan"
  ]
}
