# Local Rendering Fallback

Use the local renderer only when no image-generation tool is available or the user explicitly requests a fully local workflow.

## Behavior

The renderer converts `project.json` into deterministic SVG compositions and exports PNG files locally. It preserves:

- `1080 × 1440` for the cover by default;
- `1080 × 1920` for information pages by default;
- exact Chinese copy;
- stable filenames;
- mobile-first knowledge-card layouts.

It does not reproduce model-generated character illustration quality. Treat the local result as a complete information-card fallback, not as proof that a generative image model was used.

## Command

```bash
python3 scripts/render_xiaohongshu_project.py \
  /absolute/path/project.json \
  --output-dir /absolute/path/output
```

Use `--prompts-only` to create converted prompts without rendering. Use `--keep-svg` only when editable SVG sources are useful.

## Renderer priority

The existing engine tries:

1. `rsvg-convert`;
2. `inkscape`;
3. macOS `sips`;
4. `qlmanage`;
5. ImageMagick `magick`;
6. the optional script in `FREE_IMAGEGEN_EXPORT_SCRIPT`.

If none is available, report the missing renderer and provide the generated prompt files.

## Local page mapping

- definition or article explanation → `article_page`;
- capability grid or grouped tools → `catalog`;
- steps or mechanism → `mechanism`;
- before/after → `comparison`;
- ordered workflow → `flow`;
- chronological material → `timeline`;
- closing recommendations → `checklist`.

The local adapter may choose a stable card layout when a comic scene cannot be represented faithfully.
