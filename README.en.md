# xhs-imagen

[简体中文](./README.md)

> Give it a topic. Get a publish-ready Xiaohongshu carousel: research, copy, storyboards, character-consistent images, and QA.

`xhs-imagen` is a cross-agent skill for producing complete Xiaohongshu image-and-text posts. It goes beyond prompt writing by combining factual accuracy, mobile-first reading, visual storytelling, character consistency, and repair-oriented quality review in one workflow.

It works with Claude Code, OpenCode, OpenClaw, Hermes, Codex, and other agents that can read `SKILL.md` and invoke local scripts or image-generation tools.

## What it does

- Researches and fact-checks a topic, article, document, or rough idea
- Writes the Xiaohongshu title, post copy, hashtags, and visual narrative
- Selects pages by cognitive anchors instead of splitting source text mechanically
- Designs an original visual metaphor for every page
- Creates a 3:4 cover and 9:16 content pages
- Provides six character-and-style-bound visual profiles
- Prefers an available image model and falls back to deterministic local SVG-to-PNG rendering
- Reviews every image for text, composition, ratio, factual accuracy, and character drift
- Keeps page ordering in filenames instead of rendering page numbers into the artwork

## Quick start

```bash
git clone https://github.com/NimaChu/xhs-imagen.git
cd xhs-imagen
```

Install the repository according to your agent's skill-directory convention, or ask the agent to read the root `SKILL.md`.

```text
Use $xhs-imagen to research why RAG is not the same as installing knowledge
into a model, then create one 3:4 cover, six 9:16 explainer pages,
and publishable Xiaohongshu copy.
```

Select a visual profile when you want a specific identity:

```text
Use $xhs-imagen with toolbox-bot-risograph to create a Xiaohongshu carousel
about ten useful Codex plugins.
```

## Six built-in visual profiles

Each `visual_profile` binds the character identity, medium, palette, best-fit topics, and anti-drift constraints. An image-generation call receives only the selected profile's `character-sheet.png`.

<table>
  <tr>
    <td width="50%" valign="top">
      <strong>alpaca-line-art (default)</strong><br>
      White alpaca creator × minimal black-line drawing. Best for crisp explainers and lightweight commentary.
      <br><br>
      <img src="./assets/characters/alpaca-line-art/character-sheet.png" alt="alpaca-line-art character sheet">
    </td>
    <td width="50%" valign="top">
      <strong>glasses-chibi-blue</strong><br>
      Glasses-wearing host × cobalt-blue knowledge comic. Best for beginner education and denser cards.
      <br><br>
      <img src="./assets/characters/glasses-chibi-blue/character-sheet.png" alt="glasses-chibi-blue character sheet">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <strong>toolbox-bot-risograph</strong><br>
      Toolbox robot × two-color risograph. Best for Codex, plugins, Skills, Agents, and workflows.
      <br><br>
      <img src="./assets/characters/toolbox-bot-risograph/character-sheet.png" alt="toolbox-bot-risograph character sheet">
    </td>
    <td width="50%" valign="top">
      <strong>maker-girl-editorial</strong><br>
      Adult woman engineer × modern editorial illustration. Best for AI Coding, workplace tutorials, and opinion.
      <br><br>
      <img src="./assets/characters/maker-girl-editorial/character-sheet.png" alt="maker-girl-editorial character sheet">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <strong>cyber-luban-woodcut</strong><br>
      Jointed Luban craftsperson × new-Chinese woodcut. Best for Skill–Harness–Agent architecture and system building.
      <br><br>
      <img src="./assets/characters/cyber-luban-woodcut/character-sheet.png" alt="cyber-luban-woodcut character sheet">
    </td>
    <td width="50%" valign="top">
      <strong>capybara-gouache</strong><br>
      Capybara operations helper × warm opaque gouache. Best for beginner explainers, pitfalls, and everyday analogies.
      <br><br>
      <img src="./assets/characters/capybara-gouache/character-sheet.png" alt="capybara-gouache character sheet">
    </td>
  </tr>
</table>

Character assets live at:

```text
assets/characters/<profile-id>/character-sheet.png
```

Each sheet includes multiple views, expressions, core actions, and fixed props for cross-page identity control.

## Workflow

1. Resolve the audience, outcome, page count, language, and visual profile.
2. Research current or disputed claims and separate facts from analogies.
3. Select cognitive anchors that materially change what the reader understands.
4. Turn each abstract idea into a physical action and an ordinary object.
5. Make the selected character cause, block, repair, transform, or reveal the key relationship.
6. Generate the cover and one representative page before locking the style.
7. Produce the full series, repair defects, and recheck every page.

## Default output

```text
output/<topic-slug>/
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

| Asset | Ratio | Recommended size |
|---|---:|---:|
| Cover | 3:4 | 1080 × 1440 |
| Content page | 9:16 | 1080 × 1920 |

The default package contains one cover and five to eight information pages, with one dominant idea per page.

## Rendering paths

| Condition | Path | Result |
|---|---|---|
| Image-generation tool available | Generate with the selected profile's only character reference | Expressive illustrations suitable for publishing |
| No image-generation tool | Render deterministic SVG-to-PNG knowledge cards locally | Stable Chinese text and reproducible output |

Use the SVG text patch only after the user explicitly reports incorrect or unreadable text in an existing image.

## Local tools

```bash
python3 scripts/validate_project.py references/project.template.json

python3 scripts/make_prompt_pack.py \
  references/project.template.json \
  --output-dir output/demo/prompts

python3 scripts/render_xiaohongshu_project.py \
  references/project.template.json \
  --output-dir output/demo
```

The local renderer tries `rsvg-convert`, Inkscape, macOS `sips` / `qlmanage`, ImageMagick, or a custom exporter configured through `FREE_IMAGEGEN_EXPORT_SCRIPT`.

## Add your own profile

1. Create `assets/characters/<profile-id>/character-sheet.png`.
2. Register its identity, style lock, negative constraints, and patch background in `references/visual-profiles.json`.
3. Add immutable traits and drift checks to `references/character-consistency.md`.
4. Run validation and tests.

Treat the character and art direction as one inseparable profile, with exactly one character reference per profile.

## Tests

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_project.py references/project.template.json
python3 scripts/make_prompt_pack.py references/project.template.json --output-dir /tmp/xhs-prompts
python3 scripts/render_xiaohongshu_project.py references/project.template.json --output-dir /tmp/xhs-render --prompts-only
```

## Compatibility

The original `scripts/free_image_gen.py` CLI and Story Plan interfaces remain available for existing local workflows. `agents/openai.yaml` supplies optional client UI metadata and does not tie the skill to any one agent.

## License

MIT
