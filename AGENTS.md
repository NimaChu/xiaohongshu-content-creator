# Repository guidance

This repository contains the `xhs-imagen` Agent Skill and dependency-free helper scripts.

## Required checks

Run before completing a change:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py references/project.template.json
python3 scripts/make_prompt_pack.py references/project.template.json --output-dir /tmp/xhs-prompts
python3 scripts/render_xiaohongshu_project.py references/project.template.json --output-dir /tmp/xhs-render --prompts-only
```

When images were rendered, also run:

```bash
python3 scripts/check_png_ratios.py /tmp/xhs-render/images
```

## Editing rules

- Keep Xiaohongshu creation and publishing needs as the primary product scope.
- Keep `SKILL.md` concise and route detail into `references/`.
- Preserve the default 3:4 cover and 9:16 inner-page conventions.
- Prefer an available image-generation tool; use the local renderer only when it is unavailable.
- Use SVG text patching only after explicit user feedback about a text defect.
- Keep the legacy `free_image_gen.py` CLI compatible unless a breaking change is intentional.
- Do not commit source portraits, credentials, generated watermarks, `__pycache__`, or unlicensed fonts.
- Use only Python standard library unless a dependency is clearly justified.
