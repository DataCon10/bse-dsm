# Cheat Sheet

Exam reference for *Mathematics for Machine Learning* (Deisenroth, Faisal & Ong), Chapters 2–5 plus least squares and PCA.

## Files

| File | Role |
|---|---|
| `linear-algebra.md` | **source of truth** — edit this |
| `build.py` | wraps the markdown into the HTML page |
| `linear-algebra.html` | generated output — do not hand-edit |

## Build

```sh
python3 cheatsheet/build.py
```

Stdlib only, no dependencies.

## Print to PDF

1. Open `cheatsheet/linear-algebra.html` in Chrome or Safari
2. Wait for the maths to render (no raw `$` signs should remain)
3. Cmd+P → Destination **Save as PDF**
4. Enable **Background graphics** so table headers and callouts keep their shading

Each top-level section starts on a new page, and tables and formulas are prevented from splitting across page breaks.

## Note

marked.js and KaTeX load from a CDN, so you need internet access **when rendering**. The exported PDF is self-contained.
