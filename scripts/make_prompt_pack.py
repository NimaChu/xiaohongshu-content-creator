#!/usr/bin/env python3
"""Generate per-page image-model prompts from a Xiaohongshu project."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validate_project import load_and_validate, resolve_visual_profile


def quote_lines(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines if line)


def cognitive_anchor_text(value: dict[str, Any]) -> str:
    return f"- Type: {value['type']}\n- Why this deserves a page: {value['reason']}"


def metaphor_text(value: dict[str, Any]) -> str:
    return (
        f"- Abstract concept: {value['concept']}\n"
        f"- Physical action: {value['physical_action']}\n"
        f"- Ordinary object: {value['everyday_object']}"
    )


def cover_prompt(project: dict[str, Any]) -> str:
    cover = project["cover"]
    profile_id, profile = resolve_visual_profile(project)
    width = cover.get("width", 1080)
    height = cover.get("height", 1440)
    exact = [cover["title"], cover.get("subtitle", ""), cover.get("bottom_takeaway", "")]
    return f"""# 00 Cover — 3:4

生成一张竖版 3:4 小红书漫画图文封面，输出 {width}×{height}。

## Topic
{project['topic']}

## Audience
{project['audience']}

## Visual profile
{profile_id} — {profile['label']}

## Exact copy
{quote_lines(exact)}

## Cognitive anchor
{cognitive_anchor_text(cover['cognitive_anchor'])}

## Original visual metaphor — three steps
{metaphor_text(cover['metaphor'])}

## Composition
{cover['composition']}

## Core character action
{cover['character_action']}

## Character
{profile['character']}

## Character reference
Use `{profile['character_reference']}` as the only image reference. Preserve identity, not the reference composition.

## Style lock
{profile['style_lock']}

## Negative constraints
{profile['negative_constraints']}

确保封面在缩略图尺寸下仍能读清主题。不要把内页的全部知识点塞进封面。
"""


def page_prompt(project: dict[str, Any], page: dict[str, Any]) -> str:
    profile_id, profile = resolve_visual_profile(project)
    width = page.get("width", 1080)
    height = page.get("height", 1920)
    exact = [page["title"], page["key_message"], *page.get("copy", [])]
    return f"""# {page['number']:02d} {page['title']} — 9:16

生成一张竖版 9:16 小红书漫画科普信息图，输出 {width}×{height}。一页只解释一个核心概念。

## Page role
- Archetype: {page['archetype']}
- Key message: {page['key_message']}

## Visual profile
{profile_id} — {profile['label']}

## Exact copy
{quote_lines(exact)}

## Cognitive anchor
{cognitive_anchor_text(page['cognitive_anchor'])}

## Original visual metaphor — three steps
{metaphor_text(page['metaphor'])}

## Visual narrative
{page['visual']}

## Core character action
{page['character_action']}

## Character pose and expression
{page['character_pose']}

## Diagram and reading flow
{page['flow']}

## Character
{profile['character']}

## Character reference
Use `{profile['character_reference']}` as the only image reference. Preserve identity, not the reference composition.

## Style lock
{profile['style_lock']}

## Negative constraints
{profile['negative_constraints']}

文本必须准确、清楚、完整。优先保留标题、核心句和关键标签；不要自行添加大段解释。
"""


def prompt_filename(page: dict[str, Any]) -> str:
    return f"{page['number']:02d}-page.md"


def write_prompts(project: dict[str, Any], output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = [output_dir / "00-cover.md"]
    paths[0].write_text(cover_prompt(project).rstrip() + "\n", encoding="utf-8")
    for page in project["pages"]:
        path = output_dir / prompt_filename(page)
        path.write_text(page_prompt(project, page).rstrip() + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    try:
        project = load_and_validate(args.project)
        paths = write_prompts(project, args.output_dir)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    for path in paths:
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
