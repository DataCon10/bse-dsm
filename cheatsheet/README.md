# Cheat Sheet

Exam reference for *Brush-Up in Mathematics, Probability & Statistics* (Dominik Wielath, BSE 2026), built from lecture notes and problem sets, cross-referenced to Deisenroth, Faisal & Ong.

## Files

| Path | Role |
|---|---|
| `src/exam-sheet.md` | **Tier 2** — dense, lookup-optimised, for use in the exam |
| `src/study-linear-algebra.md` | **Tier 1** — full intuition and derivations, for revising |
| `build.py` | renders every `src/*.md` to `out/*.html` |
| `vendor/` | KaTeX + marked, so rendering works offline |
| `out/` | generated — do not hand-edit |

Edit the markdown in `src/`; never edit `out/`.

## Build

```sh
python3 cheatsheet/build.py
```

Stdlib only, no dependencies.

## Print to PDF

```sh
open -a "Google Chrome" cheatsheet/out/exam-sheet.html
```

**Cmd+P** → Destination **Save as PDF**.

Two settings that matter:

- **Background graphics: ON** (under "More settings") — otherwise you lose table header shading and the callout bars, which is most of the visual navigation
- **Scale: 100%** — the exam profile is already tuned

Chrome's **Headers and footers** option adds page numbers; worth enabling on the exam sheet.

## Print profiles

Each source file selects its stylesheet via frontmatter:

```yaml
---
title: Exam Sheet
profile: exam
---
```

| | `exam` | `study` |
|---|---|---|
| Base font in print | 8.5pt | 10pt |
| Margins | 10mm | 14mm |
| Section breaks | none — pages packed | new page per section |

Both prevent tables, formulas and code blocks from splitting across page breaks.

## Notes

`vendor/` is ~1.5 MB and committed deliberately: it removes any dependency on network access when rendering.

`linear-algebra.md` and `linear-algebra.html` in this folder are an earlier single-file draft, superseded by `src/`. Safe to delete.
