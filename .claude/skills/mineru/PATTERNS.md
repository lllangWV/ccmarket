# Patterns and anti-patterns

## Pattern: Prefer content_list.json for downstream processing
- content_list is flat, reading-order oriented, and easier to post-process than middle.json.
- Use middle.json when hierarchical block structure is required (secondary dev).

## Pattern: Be explicit about backend differences
- Pipeline and VLM structured outputs are not interchangeable.
- Do not reuse pipeline parsers on VLM outputs without adaptation (types and fields differ).

## Pattern: Use debug PDFs to explain issues, not guess
- Use `*_layout.pdf` to reason about reading order and block detection.
- Use `*_spans.pdf` (pipeline) to diagnose missing text and inline formula issues.

## Pattern: Export tables as HTML + metadata
- Keep table HTML as authoritative.
- Include page_idx + bbox for traceability to the source.

## Pattern: Coordinate system caution
- Pipeline model.json uses quadrilateral polys in page pixel space.
- VLM model.json uses bbox normalized percentages in [0,1].
- content_list bbox is mapped to 0–1000.
Never compare coordinates across these files without conversion.

## Anti-pattern: Declaring extraction “complete” without validation
- Always confirm key output files exist and are non-empty.
- Always spot-check a few blocks in content_list (first page, a table page, a formula page).

## Anti-pattern: Overfitting settings globally
- For debugging, iterate with a narrow page range first.
- Only scale up to full-document runs after QA passes.
