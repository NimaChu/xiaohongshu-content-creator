# Visual Profiles

A visual profile binds one IP identity, one character reference image, and one default style. Choose one profile per project and store its ID in `project.json` as `visual_profile`.

## Built-in profiles

### `alpaca-line-art` — default

- Asset: `assets/characters/alpaca-line-art/character-sheet.png`
- IP: white alpaca creator
- Style: pure-white background, fine black hand-drawn lines, generous whitespace, sparse blue emphasis
- Best for: crisp knowledge explainers, conceptual metaphors, lightweight creator commentary

### `glasses-chibi-blue`

- Asset: `assets/characters/glasses-chibi-blue/character-sheet.png`
- IP: glasses-wearing chibi creator
- Style: warm off-white paper, polished black outlines, cobalt-blue brush accents, pale-blue cards
- Best for: friendly beginner education, denser knowledge cards, the repository's original visual identity

### `toolbox-bot-risograph`

- Asset: `assets/characters/toolbox-bot-risograph/character-sheet.png`
- IP: cursor-antenna toolbox robot
- Style: warm uncoated paper, deep indigo and orange-red risograph inks, grain, halftone, and slight misregistration
- Best for: Codex, plugins, Skills, Agents, tool recommendations, and workflows

### `maker-girl-editorial`

- Asset: `assets/characters/maker-girl-editorial/character-sheet.png`
- IP: adult East Asian woman engineer in a rust-red work jacket
- Style: modern magazine editorial illustration, warm ivory, navy, rust red, textured flat color, and natural adult proportions
- Best for: AI Coding, professional tutorials, workplace topics, and opinion-led content

### `cyber-luban-woodcut`

- Asset: `assets/characters/cyber-luban-woodcut/character-sheet.png`
- IP: jointed wooden Luban craftsperson with a square, apron, and toolbox
- Style: new-Chinese woodcut on fibrous xuan paper, black carved lines, wood brown, and sparse cinnabar red
- Best for: Skill–Harness–Agent architecture, system building, mechanisms, and construction metaphors

### `capybara-gouache`

- Asset: `assets/characters/capybara-gouache/character-sheet.png`
- IP: capybara operations helper in a forest-green apron
- Style: warm opaque gouache, visible dry-brush texture, caramel brown, moss green, cream, and sparse terracotta
- Best for: beginner explainers, pitfalls, reassurance, checklists, and everyday analogies

## Selection rules

1. Use the profile the user names or describes.
2. When the user asks to see choices, present the six labels, concise style differences, and best-fit topics.
3. When the user gives no preference, use the registry's `default` profile.
4. Lock the selected profile for the whole series unless the user explicitly requests a mixed series.
5. Treat each profile as an inseparable character-and-style pair. Do not combine one profile's character reference with another profile's style.
6. Attach only the selected profile's `character_reference` in each image-generation call. Never attach multiple character sheets at once.

The cognitive-anchor, original-metaphor, core-character-action, page-ratio, and repair-oriented QA rules apply to every profile.

## Adding a profile

To add another IP without changing the workflow:

1. create `assets/characters/<profile-id>/character-sheet.png` with four views, expressions, core actions, and fixed props;
2. add `<profile-id>` under `profiles` in `references/visual-profiles.json`;
3. provide `label`, `character_reference`, `character`, `style_lock`, `negative_constraints`, and `patch_background`;
4. add profile-specific identity checks to `references/character-consistency.md`;
5. validate the template or a project using the new ID.

Use lowercase letters, digits, and hyphens for profile IDs. Keep exactly one character reference image per profile.
