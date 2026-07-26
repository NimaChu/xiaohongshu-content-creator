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

## Selection rules

1. Use the profile the user names or describes.
2. When the user asks to see choices, present the two labels and concise style differences.
3. When the user gives no preference, use the registry's `default` profile.
4. Lock the selected profile for the whole series unless the user explicitly requests a mixed series.
5. Attach only the selected profile's `character_reference` in each image-generation call. Never attach both built-in character sheets at once.

The cognitive-anchor, original-metaphor, core-character-action, page-ratio, and repair-oriented QA rules apply to every profile.

## Adding a profile

To add another IP without changing the workflow:

1. create `assets/characters/<profile-id>/character-sheet.png`;
2. add `<profile-id>` under `profiles` in `references/visual-profiles.json`;
3. provide `label`, `character_reference`, `character`, `style_lock`, `negative_constraints`, and `patch_background`;
4. add profile-specific identity checks to `references/character-consistency.md`;
5. validate the template or a project using the new ID.

Use lowercase letters, digits, and hyphens for profile IDs. Keep exactly one character reference image per profile.
