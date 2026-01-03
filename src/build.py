from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def build_index(site_title: str, tools: list[dict[str, Any]]) -> str:
    # Simple, clean launcher page with relative links (works on GitHub Pages)
    tool_cards = []
    for t in tools:
        href = f"./{t['output']}"
        name = t.get("name", t["slug"])
        desc = t.get("description", "")
        tool_cards.append(
            f"""
            <a class="tool" href="{href}">
              <div class="name">{name}</div>
              <div class="desc">{desc}</div>
            </a>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{site_title}</title>
  <style>
    body {{
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      background: #0b1020;
      color: #eef1ff;
      margin: 0;
      padding: 40px;
    }}
    h1 {{ margin: 0 0 18px; }}
    .grid {{
      display: grid;
      gap: 14px;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      margin-top: 18px;
    }}
    .tool {{
      display: block;
      padding: 16px 18px;
      border-radius: 12px;
      background: rgba(255,255,255,0.08);
      text-decoration: none;
      color: inherit;
      transition: transform 0.08s ease, background 0.2s ease;
    }}
    .tool:hover {{
      background: rgba(255,255,255,0.14);
      transform: translateY(-1px);
    }}
    .name {{ font-size: 18px; font-weight: 650; }}
    .desc {{ margin-top: 6px; font-size: 13px; opacity: 0.72; line-height: 1.35; }}
    footer {{ margin-top: 40px; font-size: 12px; opacity: 0.5; }}
  </style>
</head>
<body>
  <h1>{site_title}</h1>
  <div class="grid">
    {''.join(tool_cards)}
  </div>
  <footer>Internal tools — please do not share externally</footer>
</body>
</html>
"""


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    templates_dir = root / "templates"
    docs_dir = root / "docs"
    config_path = root / "tools.json"

    cfg = load_json(config_path)
    site_title = cfg.get("site_title", "Tools")
    tools = cfg.get("tools", [])

    ensure_dir(docs_dir)

    # Generate each tool page
    for t in tools:
        template_file = t["template"]
        output_file = t["output"]
        replacements = t.get("replacements", {})

        template_path = templates_dir / template_file
        out_path = docs_dir / output_file

        html = template_path.read_text(encoding="utf-8")
        for k, v in replacements.items():
            html = html.replace(str(k), str(v))

        out_path.write_text(html, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(root)}")

    # Generate the launcher index.html
    index_html = build_index(site_title, tools)
    (docs_dir / "index.html").write_text(index_html, encoding="utf-8")
    print("Wrote docs/index.html")


if __name__ == "__main__":
    main()
