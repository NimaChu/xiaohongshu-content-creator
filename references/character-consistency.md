# Character Consistency

## Choose one profile

Resolve `visual_profile` through `references/visual-profiles.json`. Attach only its `character_reference` to each generation call. Never attach multiple profile sheets at once or mix one profile's character with another profile's style.

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

## `toolbox-bot-risograph`

Reference:

- `assets/characters/toolbox-bot-risograph/character-sheet.png`

Keep:

- horizontal rounded toolbox body with a cream rectangular face screen;
- deep-indigo case, orange-red horizontal belt, and centered silver latch;
- orange-red cursor-arrow antenna;
- segmented silver arms, orange-red pincers, short legs, and dark work boots;
- two-color indigo-and-orange risograph treatment with visible grain and slight misregistration.

Reject or repair when the robot becomes a television, generic cube, or humanoid robot; when the arrow antenna, belt, latch, pincers, or proportions drift; or when the rendering becomes glossy 3D or smooth corporate vector art.

## `maker-girl-editorial`

Reference:

- `assets/characters/maker-girl-editorial/character-sheet.png`

Keep:

- adult East Asian woman with a chin-length, side-parted black bob;
- one red pencil tucked behind the ear and no glasses;
- rust-red work jacket over a navy crewneck top;
- loose ivory straight-leg work trousers and black low shoes;
- navy crossbody tool bag and natural adult proportions;
- textured modern editorial-illustration rendering.

Reject or repair when she becomes a child, chibi, anime heroine, or photorealistic model; when glasses, long hair, skirts, or heels appear; when the pencil, jacket, trousers, shoes, or tool bag drift; or when adult proportions are lost.

## `cyber-luban-woodcut`

Reference:

- `assets/characters/cyber-luban-woodcut/character-sheet.png`

Keep:

- square carved-wood head, rectangular wood torso, and restrained expression;
- fixed joinery emblem on the chest;
- visible round wooden pins and mortise-and-tenon joints at the limbs;
- dark apron wrap, carpenter's square, and cinnabar-brown toolbox;
- black carved hatching, natural wood brown, xuan-paper fibers, and sparse cinnabar accents.

Reject or repair when the figure becomes a realistic historical person, cute round toy, metal mecha, or neon cyberpunk robot; when the square head, chest emblem, wooden pins, apron, carpenter's square, or toolbox drift; or when the style loses its carved woodblock texture.

## `capybara-gouache`

Reference:

- `assets/characters/capybara-gouache/character-sheet.png`

Keep:

- warm caramel-brown adult capybara with a thick rounded body;
- small round ears, black bead-like eyes, and a broad blunt dark muzzle;
- forest-green apron with a large front pocket;
- red pencil in the pocket and a crossbody spiral notebook;
- opaque gouache, dry-brush texture, muted warm palette, and gentle ground shadow.

Reject or repair when the character becomes a bear, hamster, beaver, guinea pig, slim animal, or plush 3D toy; when the muzzle, body proportions, apron, red pencil, or notebook drift; or when the rendering becomes glossy, vector-flat, or high-saturation.

## Core-action rule

Write `character_action` separately from `character_pose` for every image. The action must cause, block, repair, transform, or reveal the page's central relationship.

Useful actions include pulling, connecting, sorting, repairing, weighing, stamping, opening, carrying, catching, handing over, operating, guarding, and inspecting. Pointing, waving, smiling, or standing beside a finished diagram does not count as a core action.

Apply the dependency test: if removing the character leaves the metaphor fully intact, redesign the scene. The IP is an actor, not a mascot or sticker.

## Adding or replacing a character

Follow `references/visual-profiles.md`. Give each IP its own profile directory and exactly one `character-sheet.png`. Add immutable identity traits and drift checks here. Do not publish a source portrait without explicit permission.
