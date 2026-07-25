---
name: xiaohongshu-content-creator
description: Create complete Xiaohongshu image-and-text posts from a topic, article, document, or rough idea, including research, fact checking, post copy, pagination, storyboards, a 3:4 cover, 9:16 content pages, image generation or fully local SVG-to-PNG fallback, and final quality review. Use for 小红书图文、小红书封面、知识卡片、漫画科普、文章转图片、AI/科技科普图组、逐页生图提示词, or revisions to an existing Xiaohongshu series. Prefer an available image-generation model; use the bundled local renderer only when no image-generation tool is available. Apply an SVG text patch only after the user explicitly reports incorrect or unreadable text in an image.
---

# Xiaohongshu Content Creator

Turn one topic or source article into a publication-ready Xiaohongshu post package.

## Required result

Create:

```text
output/<topic-slug>/
├── project.json
├── research.md
├── post.md
├── storyboard.md
├── prompts/
│   ├── 00-cover.md
│   ├── 01-*.md
│   └── ...
├── images/
│   ├── cover.png
│   ├── page-01.png
│   └── ...
└── qa-report.md
```

If the user requests only part of the package, create only that part. Never claim that images were generated when no image-generation or local SVG renderer was available.

## Fixed Xiaohongshu defaults

- Create a `3:4` cover, recommended `1080 × 1440`.
- Create `9:16` information pages, recommended `1080 × 1920`.
- Default to one cover plus 5–8 information pages.
- Use Simplified Chinese unless requested otherwise.
- Explain one dominant idea per page.
- Optimize titles and labels for phone reading.
- Use the bundled glasses-wearing chibi host and visual system unless the user supplies another character or brand direction.

Read [references/visual-style.md](references/visual-style.md) and [references/character-consistency.md](references/character-consistency.md) before producing images.

## Workflow

### 1. Resolve the brief

Determine or infer:

- topic, audience, and desired outcome;
- the single sentence readers should remember;
- source material and whether facts may have changed;
- page count and language;
- character, palette, and brand constraints;
- whether the user wants a complete package, images, copy, or prompts.

Use beginner-friendly AI/technology education as the default audience and tone when the request does not specify them.

### 2. Research before writing

Search primary and authoritative sources for current, technical, disputed, product-specific, numerical, legal, or attributed claims. Write a claim table to `research.md`. Separate sourced facts from analogies and editorial framing.

Read [references/fact-checking.md](references/fact-checking.md) for detailed rules.

### 3. Build the content arc

Create:

- one thesis;
- one useful analogy;
- one misconception;
- 4–7 supporting ideas;
- one limitation, boundary, or human-control point;
- one final takeaway.

Write `post.md` with a Xiaohongshu title, publishable body copy, optional source note, and relevant hashtags. Write `storyboard.md` before generating images.

Read [references/content-planning.md](references/content-planning.md) when choosing page structures and reducing copy.

### 4. Create and validate the project

Store exact content and page decisions in `project.json`. Start from [references/project.template.json](references/project.template.json) and follow [references/project.schema.json](references/project.schema.json).

Validate it:

```bash
python3 scripts/validate_project.py /absolute/path/project.json
```

Generate the image-model prompt files:

```bash
python3 scripts/make_prompt_pack.py \
  /absolute/path/project.json \
  --output-dir /absolute/path/output/prompts
```

### 5. Choose the rendering path automatically

#### When an image-generation tool is available

Use it as the default path.

1. Use `assets/character-sheet.png` and `assets/character-poses.png` as image references.
2. Generate the cover and one representative inner page first.
3. Inspect character identity, typography, spacing, color, and copy accuracy.
4. Lock the successful visual description.
5. Generate the remaining pages using the same references and style lock.
6. Save files as `cover.png`, `page-01.png`, and so on.

Do not invoke the local renderer merely to pre-empt possible text errors.

#### When no image-generation tool is available

Use the bundled local SVG-to-PNG renderer:

```bash
python3 scripts/render_xiaohongshu_project.py \
  /absolute/path/project.json \
  --output-dir /absolute/path/output
```

This path preserves the Xiaohongshu cover and inner-page ratios while converting the project into deterministic local knowledge-card layouts. Read [references/local-rendering.md](references/local-rendering.md) for limitations and renderer requirements.

### 6. Repair text only after explicit user feedback

Do not create a separate hybrid workflow. If the user explicitly identifies incorrect, corrupted, or unreadable text in an existing image:

1. Confirm the target image, exact replacement text, and affected region.
2. Prefer local image editing or regeneration when available.
3. If the problem remains, apply a deterministic SVG overlay only to that region:

```bash
python3 scripts/patch_image_text.py \
  --input /absolute/path/page.png \
  --output /absolute/path/page-fixed.png \
  --x 100 --y 300 --width 880 --height 180 \
  --text "正确文字"
```

4. Inspect the repaired image before delivery.

Never apply an SVG text patch speculatively.

### 7. Inspect every output

Write `qa-report.md` and verify:

- correct ratio and orientation;
- readable, accurate Chinese and product names;
- one dominant idea per page;
- stable character, outfit, glasses, hair, and proportions;
- valid diagram flow;
- no cropped titles, faces, hands, or summaries;
- no unsupported factual claims or invented quotations;
- ordered, stable filenames.

Run:

```bash
python3 scripts/check_png_ratios.py /absolute/path/output/images
```

Read [references/quality-checklist.md](references/quality-checklist.md) for the full review.

## Final response

Provide:

- a concise summary of the content arc;
- the cover and ordered pages, or links to their files;
- the publishable post copy;
- source citations for time-sensitive claims;
- an honest note about any unresolved image or text defect.
