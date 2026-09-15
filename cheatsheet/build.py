#!/usr/bin/env python3
"""Render every markdown file in src/ to a self-contained HTML page in out/.

Stdlib only. Markdown is embedded verbatim rather than fetched, so output works
when opened directly over file:// without a local server.

Each source file carries frontmatter selecting its print stylesheet:

    ---
    title: Exam Sheet
    profile: exam
    ---
"""

from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "src"
OUT = HERE / "out"

# Local copies are used when present; otherwise fall back to the CDN.
ASSETS = {
    "katex_css": ("vendor/katex.min.css", "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css"),
    "katex_js": ("vendor/katex.min.js", "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"),
    "autorender": ("vendor/auto-render.min.js", "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"),
    "marked": ("vendor/marked.min.js", "https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"),
}

SHARED_CSS = """
  :root { --rule: #d0d0d0; --muted: #555; --accent: #1a4a7a; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    margin: 0 auto;
    color: #111;
  }

  h1 { border-bottom: 3px solid var(--accent); padding-bottom: .15em; margin-top: 0; }
  h2 { color: var(--accent); border-bottom: 1.5px solid var(--rule); padding-bottom: .1em; }
  h3 { margin-bottom: .3em; }
  h4 { color: var(--muted); margin-bottom: .2em; }

  table { border-collapse: collapse; width: 100%; margin: .5em 0; }
  th, td { border: 1px solid var(--rule); padding: .25em .45em; text-align: left; vertical-align: top; }
  th { background: #f2f5f8; font-weight: 600; }

  code { background: #f4f4f4; padding: .1em .25em; border-radius: 3px; font-size: .9em; }
  pre { background: #f7f7f7; padding: .5em .7em; border-radius: 4px; overflow-x: auto; line-height: 1.25; }
  pre code { background: none; padding: 0; }

  blockquote {
    border-left: 3px solid var(--accent); margin: .5em 0; padding: .15em .8em;
    background: #f7fafd; color: #333;
  }

  hr { border: none; border-top: 1px solid var(--rule); margin: 1.2em 0; }
  ul, ol { margin: .3em 0; padding-left: 1.3em; }
  li { margin: .1em 0; }
  .katex-display { margin: .4em 0; }
"""

PROFILES = {
    "exam": """
  body { font-size: 9.5pt; line-height: 1.35; max-width: 56em; padding: 1em; }
  h1 { font-size: 17pt; }
  h2 { font-size: 12.5pt; margin-top: 1.1em; }
  h3 { font-size: 10.5pt; margin-top: .7em; }
  h4 { font-size: 9.5pt; margin-top: .5em; }
  table { font-size: 8.5pt; }
  pre { font-size: 8pt; }

  @page { margin: 10mm; }

  @media print {
    body { max-width: none; padding: 0; font-size: 8.5pt; }
    table { font-size: 7.8pt; }
    h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
    table, pre, blockquote, tr { break-inside: avoid; page-break-inside: avoid; }
    .katex-display { break-inside: avoid; page-break-inside: avoid; }
  }
""",
    "study": """
  body { font-size: 10.5pt; line-height: 1.5; max-width: 50em; padding: 1.5em; }
  h1 { font-size: 20pt; }
  h2 { font-size: 15pt; margin-top: 1.8em; }
  h3 { font-size: 12pt; margin-top: 1.2em; }
  h4 { font-size: 10.5pt; margin-top: .8em; }
  table { font-size: 10pt; }
  pre { font-size: 9pt; }

  @page { margin: 14mm; }

  @media print {
    body { max-width: none; padding: 0; font-size: 10pt; }
    h1, h2, h3, h4 { break-after: avoid; page-break-after: avoid; }
    table, pre, blockquote, tr { break-inside: avoid; page-break-inside: avoid; }
    .katex-display { break-inside: avoid; page-break-inside: avoid; }
    h2 { break-before: page; page-break-before: page; }
    h2:first-of-type { break-before: auto; page-break-before: auto; }
  }
""",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="{katex_css}">
<style>{shared_css}{profile_css}</style>
</head>
<body>
<div id="content">Rendering&hellip;</div>

<script type="text/markdown" id="source">{markdown}</script>
<script src="{marked}"></script>
<script src="{katex_js}"></script>
<script src="{autorender}"></script>
<script>
  var raw = document.getElementById('source').textContent;

  // Shield math from the markdown parser: underscores and asterisks inside
  // formulas would be eaten as emphasis, and \\| inside a table cell would be
  // read as a column delimiter.
  var stash = [];
  function shield(match) {{
    stash.push(match);
    return 'ZMATHZ' + (stash.length - 1) + 'ZENDZ';
  }}
  raw = raw.replace(/\\$\\$[\\s\\S]+?\\$\\$/g, shield);
  raw = raw.replace(/\\$[^$\\n]+?\\$/g, shield);

  var html = marked.parse(raw);

  // Escape on restore: this string goes through innerHTML, so a "<" or ">"
  // inside a formula would otherwise be parsed as an HTML tag and eaten.
  function escapeHtml(s) {{
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }}
  html = html.replace(/ZMATHZ(\\d+)ZENDZ/g, function (_, i) {{ return escapeHtml(stash[+i]); }});

  var target = document.getElementById('content');
  target.innerHTML = html;

  renderMathInElement(target, {{
    delimiters: [
      {{ left: '$$', right: '$$', display: true }},
      {{ left: '$', right: '$', display: false }}
    ],
    throwOnError: false
  }});
</script>
</body>
</html>
"""


def asset(key: str) -> str:
    local, cdn = ASSETS[key]
    return f"../{local}" if (HERE / local).exists() else cdn


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    _, block, body = text.split("---\n", 2)
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, body.lstrip("\n")


def render(path: Path) -> Path:
    meta, body = split_frontmatter(path.read_text(encoding="utf-8"))
    profile = meta.get("profile", "study")
    if profile not in PROFILES:
        raise ValueError(f"{path.name}: unknown profile {profile!r}")

    # A literal </script> in the source would close the embedding block early.
    body = body.replace("</script", "<\\/script")

    OUT.mkdir(exist_ok=True)
    target = OUT / f"{path.stem}.html"
    target.write_text(
        TEMPLATE.format(
            title=meta.get("title", path.stem),
            shared_css=SHARED_CSS,
            profile_css=PROFILES[profile],
            markdown=body,
            katex_css=asset("katex_css"),
            katex_js=asset("katex_js"),
            autorender=asset("autorender"),
            marked=asset("marked"),
        ),
        encoding="utf-8",
    )
    return target


def main() -> None:
    sources = sorted(SRC.glob("*.md"))
    if not sources:
        raise SystemExit(f"no markdown found in {SRC}")

    offline = (HERE / ASSETS["katex_js"][0]).exists()
    print(f"assets: {'vendored (works offline)' if offline else 'CDN (needs internet to render)'}")

    for src in sources:
        out = render(src)
        print(f"  {src.name:30} -> {out.relative_to(HERE)}  ({len(src.read_text()):,} chars)")


if __name__ == "__main__":
    main()
