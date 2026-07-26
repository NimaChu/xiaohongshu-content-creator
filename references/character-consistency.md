# Character Consistency

## Choose one profile

Resolve `visual_profile` through `references/visual-profiles.json`. Attach only its `character_reference` to each generation call. Never attach both built-in sheets at once.

The selected image is an identity reference, not a fixed composition. Change pose, expression, viewing angle, and props while preserving the profile-specific identity.

## `alpaca-line-art`

Reference:

- `assets/characters/alpaca-line-art/character-sheet.png`

Keep:

- white fluffy alpaca/llama-like silhouette;
- two upright tapered ears;
- large rounded muzzle with the same small three-lobed nose-and-mouth mark;
- simple black facial features and short rounded forelimbs;
- compact proportions and fine black hand-drawn line treatment.

The laptop and carrot mark are props from the reference scene, not required anatomy. Sparkle eyes are one allowed expression, not the only expression.

Reject or repair when the alpaca becomes a generic bear, cat, rabbit, or human; when the ears, muzzle, face mark, silhouette, or proportions drift; or when the line work becomes thick commercial vector art.

## `glasses-chibi-blue`

Reference:

- `assets/characters/glasses-chibi-blue/character-sheet.png`

Keep:

- young East Asian male creator;
- short, slightly tousled black hair;
- clear gray rectangular glasses;
- large warm brown eyes and friendly expression;
- charcoal crewneck sweatshirt, black trousers, and white sneakers;
- polished chibi proportions, clean black outlines, and restrained soft shading.

Reject or repair when the glasses disappear or change, hair or clothes drift, the host becomes a child or realistic adult, proportions change, or the illustration style no longer matches the approved cover.

## Core-action rule

Write `character_action` separately from `character_pose` for every image. The action must cause, block, repair, transform, or reveal the page's central relationship.

Useful actions include pulling, connecting, sorting, repairing, weighing, stamping, opening, carrying, catching, handing over, operating, guarding, and inspecting. Pointing, waving, smiling, or standing beside a finished diagram does not count as a core action.

Apply the dependency test: if removing the character leaves the metaphor fully intact, redesign the scene. The IP is an actor, not a mascot or sticker.

## Adding or replacing a character

Follow `references/visual-profiles.md`. Give each IP its own profile directory and exactly one `character-sheet.png`. Add immutable identity traits and drift checks here. Do not publish a source portrait without explicit permission.
