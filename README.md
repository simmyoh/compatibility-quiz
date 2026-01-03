# Static Tools Template (Python → GitHub Pages)

This repo is a template for building small HTML tools from templates using a Python build step,
and hosting the generated output via GitHub Pages.

## Structure
- `src/build.py` — generator script
- `templates/` — HTML templates
- `tools.json` — tool registry + replacement values
- `docs/` — generated site (served by GitHub Pages)

## Build locally
```bash
python src/build.py
