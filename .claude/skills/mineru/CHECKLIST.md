
---

# `CHECKLIST.md`

```markdown
# Pre-ship checklist — MinerU Skill

## Inputs
- [ ] Confirm input path(s) exist and are readable
- [ ] Confirm whether processing is single-file or batch directory
- [ ] Confirm whether user needs markdown, structured JSON, debug PDFs, or all

## Configuration
- [ ] Select backend (pipeline vs VLM) and justify choice
- [ ] If pipeline: select method (auto/txt/ocr) and language if OCR is expected
- [ ] Set page range for fast iteration when debugging
- [ ] Confirm table/formula toggles match user priorities
- [ ] Confirm model source (huggingface/modelscope/local) if relevant

## Execution
- [ ] Run MinerU with explicit flags
- [ ] Capture command used in the report for reproducibility

## Output validation
- [ ] Verify `*.md` exists and is non-empty
- [ ] Verify `*_content_list.json` exists and parses as JSON
- [ ] Verify `*_middle.json` and `*_model.json` exist (if expected)
- [ ] Verify `*_layout.pdf` exists
- [ ] If pipeline: check whether `*_spans.pdf` exists; if not, note it

## QA
- [ ] Spot-check reading order using `*_content_list.json`
- [ ] For issues: inspect `*_layout.pdf`; for pipeline text-loss: inspect `*_spans.pdf`
- [ ] If issues found: rerun with adjusted backend/method/lang/toggles or smaller page range

## Deliverables
- [ ] Provide the extraction report (TEMPLATES.md)
- [ ] Provide requested exports (tables/images/text) in agreed formats
- [ ] Document known limitations and recommended next iteration steps
