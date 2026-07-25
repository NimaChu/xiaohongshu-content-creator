# Xiaohongshu Content Creator

[简体中文](./README.md)

A cross-agent skill for creating complete Xiaohongshu image-and-text posts. It is not tied to one coding assistant or runtime: Claude Code, OpenCode, OpenClaw, Hermes, Codex, and any other agent that can read `SKILL.md` and invoke local scripts or image tools can use it.

The skill covers research, fact checking, post copy, pagination, storyboards, image generation, local rendering fallback, and final QA.

## Production paths

- When an image-generation tool is available, create character-consistent comic explainers using the bundled character reference.
- When no image-generation tool is available, render deterministic SVG-to-PNG knowledge cards locally.
- Apply a local SVG text patch only after the user explicitly reports incorrect or unreadable text.

Both paths use the same Xiaohongshu defaults:

| Asset | Ratio | Recommended size |
|---|---:|---:|
| Cover | 3:4 | 1080 × 1440 |
| Content page | 9:16 | 1080 × 1920 |

## Skill output

```text
output/<topic>/
├── project.json
├── research.md
├── post.md
├── storyboard.md
├── prompts/
├── images/
│   ├── cover.png
│   └── page-01.png
└── qa-report.md
```

## Use with different agents

Clone the repository:

```bash
git clone https://github.com/NimaChu/xiaohongshu-content-creator.git
cd xiaohongshu-content-creator
```

Install it according to the skill-directory convention of Claude Code, OpenCode, OpenClaw, Hermes, Codex, or your chosen agent. You can also ask the agent to read the root `SKILL.md` directly. If the agent supports `$skill-name` invocation, use:

```text
Use $xiaohongshu-content-creator to research RAG and create one 3:4 cover
plus six 9:16 Xiaohongshu comic explainer pages.
```

Otherwise, use:

```text
Read this repository's SKILL.md, research RAG, and create one 3:4 cover
plus six 9:16 Xiaohongshu comic explainer pages.
```

## Local fallback

Validate a project:

```bash
python3 scripts/validate_project.py references/project.template.json
```

Render it locally:

```bash
python3 scripts/render_xiaohongshu_project.py \
  references/project.template.json \
  --output-dir output/terminal
```

Generate image-model prompts:

```bash
python3 scripts/make_prompt_pack.py \
  references/project.template.json \
  --output-dir output/terminal/prompts
```

## Compatibility

The original `scripts/free_image_gen.py` CLI and its story-plan references remain available for existing local-rendering workflows. `agents/openai.yaml` provides optional client UI metadata and does not restrict the skill to any one agent.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py references/project.template.json
python3 scripts/check_png_ratios.py output/terminal/images
```

## License

MIT
