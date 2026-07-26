# Quality Checklist

## Content

- [ ] The series has one clear thesis.
- [ ] Every page has a named cognitive anchor and teaches one idea.
- [ ] Removing any page would remove a distinct piece of understanding.
- [ ] The progression is logical for the audience.
- [ ] Current or precise facts are sourced.
- [ ] Analogies are not presented as literal definitions.
- [ ] Named tools, products, and commands are correct.
- [ ] Limitations and human control are represented accurately.

## Copy

- [ ] The cover is readable as a thumbnail.
- [ ] Titles are short and concrete.
- [ ] No long paragraph appears inside an image.
- [ ] Chinese text and English product names are exact.
- [ ] Repeated phrases are removed.
- [ ] The bottom takeaway adds value.

## Visual design

- [ ] The cover is 3:4.
- [ ] Every information page is 9:16.
- [ ] The background, line treatment, and palette match the selected visual profile.
- [ ] `alpaca-line-art`: pure white, fine black hand-drawn lines, sparse accent color.
- [ ] `glasses-chibi-blue`: warm off-white paper, polished black outlines, cobalt-blue accents.
- [ ] Every page uses one original physical metaphor and one primary structure.
- [ ] The character performs the core action; removing it would break the metaphor.
- [ ] The selected profile's immutable character traits and proportions are stable.
- [ ] Arrows and diagrams are semantically correct.
- [ ] The hierarchy is obvious within two seconds.
- [ ] No title, hand, face, or bottom strip is cropped.
- [ ] Whitespace is sufficient.
- [ ] No visible page number, page count, or page-position marker appears. Numbers are used only when they explain ordered content steps.

## Image defects

- [ ] No malformed hands distract from the point.
- [ ] No accidental duplicated characters or objects appear.
- [ ] No corrupted labels, commands, or product names remain.
- [ ] No unwanted watermark or platform mark appears.
- [ ] No page drifts away from the approved visual direction.

## Delivery

- [ ] Files are named `cover.png`, `page-01.png`, and so on.
- [ ] `project.json`, post copy, storyboard, prompts, research, and QA are included when requested.
- [ ] `qa-report.md` lists repaired and unresolved defects honestly.
- [ ] SVG text patching was used only after explicit user feedback.

## Repair playbook

For each failure, repair the image or prompt and then run the same check again. Record `defect → repair → recheck result` in `qa-report.md`.

| Failure | Required repair | Pass condition |
|---|---|---|
| Weak or redundant page | Remove it, merge it with a neighboring anchor, or rewrite the cognitive anchor | The page has one distinct answer to “what understanding is lost if removed?” |
| Character is decorative | Replace pointing/standing with an action that causes, blocks, repairs, transforms, or reveals the result | Removing the character breaks the metaphor |
| Metaphor is generic or copied | Keep the concept; replace both the physical verb and primary object | The scene is topic-specific and not repeated elsewhere in the series |
| Page looks like PPT | Remove grids, frames, type labels, and excess arrows; rebuild around one physical scene | One primary structure is legible within two seconds |
| Background or lines mismatch | Restate the selected profile's `style_lock`; for alpaca remove paper color and thick lines, for glasses chibi restore warm paper and polished outlines | Background and line treatment match the selected profile |
| Character identity drifts | Reattach only the selected profile's `character_reference` and restate its immutable traits | The character matches the selected profile |
| Page is too dense | Remove secondary objects and labels; keep one object plus at most two supports | Main cluster uses roughly 40–65% of the canvas with clear quiet space |
| Text is too long | Move explanation to `post.md`; retain only title, anchor sentence, and short labels | All image text is readable at phone size |
| Text is wrong or unreadable | Regenerate or edit locally; use SVG overlay only after explicit user feedback | Exact required copy is legible and correct |
| Crop or ratio is wrong | Recompose inside safe margins and export again | Cover is 3:4; pages are 9:16; no key element is clipped |
| Page number or page-position marker appears | Remove `04`, `01/08`, `PAGE 04`, or any equivalent pagination badge; keep order in filenames only | No pagination marker is visible; meaningful content-step numbers may remain |
| Fact or product detail is unsupported | Correct from a primary source or remove the claim | `research.md` supports the final wording |
