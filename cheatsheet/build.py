#!/usr/bin/env python3
"""Wrap linear-algebra.md into a self-contained HTML page for print-to-PDF.

Stdlib only. The markdown is embedded verbatim rather than fetched, so the
output works when opened directly over file:// without a local server.
"""

from pathlib import Path

HERE = Path(__file__).parent
SOURCE = HERE / "linear-algebra.md"
OUTPUT = HERE / "linear-algebra.html"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Linear Algebra Cheat Sheet</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>
  :root {{ --rule: #d0d0d0; --muted: #555; --accent: #1a4a7a; }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.45;
    max-width: 52em;
    margin: 0 auto;
    padding: 1.5em;
    color: #111;
  }}

  h1 {{ font-size: 20pt; border-bottom: 3px solid var(--accent); padding-bottom: .2em; margin-top: 0; }}
  h2 {{
    font-size: 14pt; color: var(--accent); border-bottom: 1.5px solid var(--rule);
    padding-bottom: .15em; margin-top: 1.6em;
  }}
  h3 {{ font-size: 11.5pt; margin-top: 1.1em; margin-bottom: .35em; }}
  h4 {{ font-size: 10.5pt; margin-top: .8em; margin-bottom: .25em; color: var(--muted); }}

  table {{ border-collapse: collapse; width: 100%; margin: .6em 0; font-size: 9.5pt; }}
  th, td {{ border: 1px solid var(--rule); padding: .3em .5em; text-align: left; vertical-align: top; }}
  th {{ background: #f2f5f8; font-weight: 600; }}

  code {{ background: #f4f4f4; padding: .1em .3em; border-radius: 3px; font-size: .9em; }}
  pre {{ background: #f7f7f7; padding: .6em .8em; border-radius: 4px; overflow-x: auto; font-size: 9pt; line-height: 1.3; }}
  pre code {{ background: none; padding: 0; }}

  blockquote {{
    border-left: 3px solid var(--accent); margin: .6em 0; padding: .2em .9em;
    background: #f7fafd; color: #333;
  }}

  hr {{ border: none; border-top: 1px solid var(--rule); margin: 1.5em 0; }}
  ul, ol {{ margin: .4em 0; padding-left: 1.4em; }}
  li {{ margin: .15em 0; }}
  .katex-display {{ margin: .5em 0; }}

  @page {{ margin: 14mm; }}

  @media print {{
    body {{ max-width: none; padding: 0; font-size: 9.5pt; }}
    h1, h2, h3, h4 {{ break-after: avoid; page-break-after: avoid; }}
    table, pre, blockquote {{ break-inside: avoid; page-break-inside: avoid; }}
    tr {{ break-inside: avoid; page-break-inside: avoid; }}
    .katex-display {{ break-inside: avoid; page-break-inside: avoid; }}
    h2 {{ break-before: page; page-break-before: page; }}
    h2:first-of-type {{ break-before: auto; page-break-before: auto; }}
  }}
</style>
</head>
<body>
<div id="content">Rendering&hellip;</div>

<script type="text/markdown" id="source">{markdown}</script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>
  var raw = document.getElementById('source').textContent;

  // Shield math from the markdown parser: underscores and asterisks inside
  // formulas would otherwise be eaten as emphasis.
  var stash = [];
  function shield(match) {{
    stash.push(match);
    return 'ZMATHZ' + (stash.length - 1) + 'ZENDZ';
  }}
  raw = raw.replace(/\\$\\$[\\s\\S]+?\\$\\$/g, shield);
  raw = raw.replace(/\\$[^$\\n]+?\\$/g, shield);

  var html = marked.parse(raw);
  html = html.replace(/ZMATHZ(\\d+)ZENDZ/g, function (_, i) {{ return stash[+i]; }});

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


def main() -> None:
    markdown = SOURCE.read_text(encoding="utf-8")
    # A literal </script> in the source would close the embedding block early.
    markdown = markdown.replace("</script", "<\\/script")
    OUTPUT.write_text(TEMPLATE.format(markdown=markdown), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(HERE.parent)} ({len(markdown):,} chars of markdown)")


if __name__ == "__main__":
    main()
