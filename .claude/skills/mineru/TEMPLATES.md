# Templates

## MinerU run plan template
- Input: [file|directory], path: `...`
- Output directory: `...`
- Backend: [pipeline|vlm-*]
- Method (pipeline only): [auto|txt|ocr]
- Language (pipeline OCR only): `...`
- Page range: start=`...`, end=`...` (0-based; optional)
- Toggles: formula=[true/false], table=[true/false]
- Model source: [huggingface|modelscope|local]
- Device: `MINERU_DEVICE_MODE=...` (optional)

## Command templates

### Pipeline default
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m auto
```


### Pipeline OCR with language
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m ocr -l en
```

### VLM transformers backend
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -b vlm-transformers
```

### Restrict page range
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -s 0 -e 4
```

### Pipeline default
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m auto
```

### Pipeline default
```bash
mineru -p "<input.pdf>" -o "<out_dir>" -b pipeline -m auto
```

## Output artifact templates

### Extraction report (markdown)

``` markdown
# MinerU Extraction Report — [document name]

## Run configuration
- Backend:
- Method:
- Language:
- Page range:
- Formula enabled:
- Table enabled:
- Model source:
- Output directory:

## Outputs produced
- Markdown: [path]
- Content list: [path]
- Middle JSON: [path]
- Model JSON: [path]
- Layout PDF: [path]
- Spans PDF (if any): [path]

## QA summary
- Reading order: [OK | issues]
- Missing text: [none | suspected areas]
- Tables: [OK | issues]
- Formulas: [OK | issues]

## Notes / recommended reruns
1. ...
```

## Tables export (JSON)


```json
[
  {
    "page_idx": 5,
    "bbox": [62, 480, 946, 904],
    "caption": ["Table 2 ..."],
    "footnote": ["..."],
    "html": "<html>...</html>"
  }
]

```

## Images manifest (JSON)


```json
[
  {
    "page_idx": 1,
    "bbox": [62, 480, 946, 904],
    "img_path": "images/<hash>.jpg",
    "caption": ["Fig. 1 ..."],
    "footnote": []
  }
]
```