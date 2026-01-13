---
name: processing-pdfs-mineru
description: Runs MinerU to parse PDFs into Markdown and structured outputs, then post-processes results (content_list.json, middle.json, model.json, layout.pdf/spans.pdf) into user-requested formats. Use when the user asks to extract text/tables/images/equations from PDFs, convert PDFs to Markdown, or debug MinerU parsing quality.
---

# Processing PDFs with MinerU

## Overview
This Skill converts PDFs (or directories of PDFs) into:
- Primary content: `*.md` and `*_content_list.json`
- Secondary development: `*_middle.json` and `*_model.json`
- Debug/QA: `*_layout.pdf` and (pipeline only) `*_spans.pdf`

It also supports post-processing: filtering content types, assembling a clean “extracted text” view, exporting tables, and generating QA summaries.

## When to use this Skill
Use this Skill when the user asks to:
- Convert a PDF to Markdown (with tables/formulas preserved when possible)
- Extract structured content (headings, paragraphs, tables, images, equations, code blocks, lists)
- Produce a “reading order” content stream
- Debug extraction quality (missing text, incorrect order, broken tables, formula issues)
- Batch-process a folder of PDFs with consistent settings

Do NOT use this Skill when:
- The user wants generic summarization without needing PDF extraction
- The input is not a document file MinerU can parse (e.g., plain images only) unless the plan is to convert to PDF first

## Environment & constraints
Assumptions (adjust if the runtime differs):
- MinerU CLI tools are available: `mineru`, optionally `mineru-api`, `mineru-gradio`
- File system access is available for reading input PDFs and writing outputs
- If using VLM backends, appropriate GPU/runtime dependencies may be required

Key MinerU knobs (CLI):
- `--backend pipeline|vlm-transformers|vlm-vllm-engine|vlm-lmdeploy-engine|vlm-http-client`
- `--method auto|txt|ocr` (pipeline only)
- `--lang ...` (pipeline OCR accuracy)
- `--start/--end` (page ranges, 0-based)
- `--formula/--table` toggles
- `--source huggingface|modelscope|local`

Environment variables (global overrides):
- `MINERU_DEVICE_MODE`, `MINERU_VIRTUAL_VRAM_SIZE`, `MINERU_MODEL_SOURCE`
- `MINERU_FORMULA_ENABLE`, `MINERU_TABLE_ENABLE`, `MINERU_TABLE_MERGE_ENABLE`, etc.

## Outputs and which to use
Prefer these defaults unless the user requests otherwise:
- **Content extraction for downstream processing:** `*_content_list.json` (flat, reading order)
- **Best-effort “document content” view:** `*.md` plus `*_content_list.json`
- **Secondary development / full structure:** `*_middle.json`
- **Raw model inspection:** `*_model.json`
- **Debug QA:** `*_layout.pdf` and (pipeline) `*_spans.pdf`

Backend awareness:
- **Pipeline**: content_list and middle are stable; `spans.pdf` can exist; coordinates differ by file type.
- **VLM**: structured outputs changed significantly vs pipeline; `model.json` format differs; additional types like code/list/discarded blocks can appear.

## Scope & triggers
### Typical triggers
- “Run MinerU on this PDF”
- “Convert to markdown”
- “Extract tables/images/equations”
- “Give me content_list.json in reading order”
- “Debug missing text / wrong order”
- “Use pipeline vs VLM backend”

### Out of scope
- Training or modifying MinerU models
- Guaranteeing perfect semantic structure for all PDFs (provide QA steps and best-effort outputs)

---

# Core workflows

## 1) Intake & planning workflow
1. Identify inputs:
   - Single PDF file vs directory of PDFs
   - Desired outputs: markdown only, structured JSON, or debugging PDFs
   - Content priorities: tables, formulas, images, code blocks, lists
2. Choose backend:
   - Use **pipeline** for traditional OCR/text extraction and stable structured outputs.
   - Use **VLM** backends when document structure is complex and VLM runtime is available.
3. Choose method (pipeline only):
   - `auto` by default; use `txt` if text-based PDF is expected; use `ocr` for scanned PDFs.
4. Choose page range (optional):
   - Use `--start/--end` to reduce cost/time and iterate quickly.
5. Decide toggles:
   - Keep formulas/tables enabled unless user requests speed over fidelity.

Deliverable from this step: an explicit run plan (backend, method, lang, range, toggles, output directory).

## 2) Execution workflow (run MinerU)
Run MinerU with explicit, reproducible flags.

Example (single file, pipeline default):
- `mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m auto`

Example (OCR focus + language):
- `mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m ocr -l en`

Example (VLM backend):
- `mineru -p "<input.pdf>" -o "<out_dir>" -b vlm-transformers`

Batch example (directory):
- `mineru -p "<input_dir>" -o "<out_dir>" -b pipeline -m auto`

After running:
1. Enumerate outputs created in the output directory.
2. Confirm existence of:
   - `*.md`
   - `*_content_list.json`
   - `*_middle.json` (expected)
   - `*_model.json` (expected)
   - `*_layout.pdf` (expected)
   - `*_spans.pdf` (pipeline only; not always present depending on mode)

## 3) Validation & QA workflow
Always validate before calling results “final”:
1. Quick completeness checks:
   - Output files exist and are non-empty
   - Page count matches expectation when a range is specified
2. Content checks using `*_content_list.json`:
   - Verify reading order seems reasonable
   - Spot-check that headings (text_level) appear where expected
   - Confirm tables/images/equations entries exist when expected
3. Debug checks:
   - Use `*_layout.pdf` to confirm layout detection and reading order labeling
   - Use `*_spans.pdf` (pipeline) to troubleshoot text loss and inline formula recognition

If validation fails:
- Adjust backend/method/lang/toggles/page range and re-run (iterate in small slices).

## 4) Post-processing workflow (produce user-requested outputs)
Prefer `*_content_list.json` as the canonical “reading order” stream.

### 4A) Produce a clean extracted-text file
1. Load `*_content_list.json`.
2. Keep entries where `type == "text"` (and optionally headings via `text_level`).
3. Optionally include equations as LaTeX blocks (`type == "equation"`).
4. Emit:
   - `extracted.txt` (plain)
   - or `extracted.md` (preserving headings and LaTeX blocks)

### 4B) Export tables
1. From `*_content_list.json`, select entries where `type == "table"`.
2. Prefer `table_body` HTML when present (pipeline content_list includes it).
3. Emit:
   - `tables.html` (concatenated HTML tables)
   - and/or `tables.json` (one object per table: caption, footnote, html, page_idx, bbox)

### 4C) Collect images with captions
1. Select `type == "image"` entries.
2. Capture `img_path`, captions, footnotes, `page_idx`, `bbox`.
3. Emit `images_manifest.json` plus a rendered `images_report.md` with captions.

### 4D) VLM-only content types (code/list/discarded)
If VLM `content_list.json` contains:
- `type == "code"`: export `code_body` and `code_caption` into `code_blocks.md`
- `type == "list"`: export `list_items` into `lists.md`
- discarded blocks: export `discarded_blocks.json` and optionally filter headers/footers in final text

## 5) Decision tree: pipeline vs VLM
If the priority is stable, predictable structured outputs and OCR/lang control:
- Use **pipeline**.

If the priority is richer semantic block typing (code/list, more discard categories) and VLM runtime is available:
- Use **VLM**.

If outputs need to be backward-compatible with prior pipeline tooling:
- Avoid VLM unless you explicitly adapt parsers.

---

# Output formats
Use these templates unless the user requests a different format:
- Extraction report: see `TEMPLATES.md`
- Tables export: see `TEMPLATES.md`
- QA summary (layout/order issues): see `TEMPLATES.md`

For patterns and anti-patterns (e.g., coordinate systems, reading order quirks), see `PATTERNS.md`.
For pre-ship checks, see `CHECKLIST.md`.
For evaluation scenarios, see `EVALS.md`.
For common failures and fixes, see `TROUBLESHOOTING.md`.
