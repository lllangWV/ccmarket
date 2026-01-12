# Troubleshooting MinerU runs

## Symptom: Missing text (pipeline)
Likely causes:
- PDF is scanned; method should be OCR
- Wrong OCR language
- Text spans dropped due to segmentation/inline formula quirks

Actions:
1. Rerun a narrow page range with `-m ocr`
2. Set `-l <lang>` (e.g., `en`)
3. Inspect `*_spans.pdf` to locate where spans are lost
4. Inspect `*_layout.pdf` to see if blocks are detected but miss-ordered

## Symptom: Reading order is wrong
Actions:
1. Inspect `*_layout.pdf` reading-order indices
2. Prefer content_list.json ordering for downstream processing
3. If consistently wrong, consider switching backend (pipeline ↔ VLM) and compare

## Symptom: Tables are garbled
Actions:
1. Confirm table parsing is enabled (CLI `-t` / env `MINERU_TABLE_ENABLE`)
2. Export table HTML from content_list entries (if present)
3. If HTML is missing/poor, rerun with alternate backend or adjust settings; validate via layout.pdf

## Symptom: Formula output is missing or broken
Actions:
1. Ensure formula parsing is enabled (`-f` / `MINERU_FORMULA_ENABLE=true`)
2. For pipeline: if document is scanned, OCR method matters; re-test on a small range
3. Validate presence of equation blocks in content_list.json

## Symptom: Out-of-memory / GPU issues (pipeline or VLM)
Actions:
- Set device explicitly (e.g., `MINERU_DEVICE_MODE=cpu` for fallback)
- For pipeline: reduce VRAM usage via `MINERU_VIRTUAL_VRAM_SIZE`
- Use page ranges for iterative runs
- If using vllm/lmdeploy, ensure only one acceleration stack is installed to avoid conflicts

## Symptom: Cannot access HuggingFace models
Actions:
- Switch model source to ModelScope (`--source modelscope` or `MINERU_MODEL_SOURCE=modelscope`)
- Or download/use local models (`--source local`) after configuring mineru.json
