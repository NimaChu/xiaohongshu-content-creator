#!/usr/bin/env python3
"""Generate per-page image-model prompts from a Xiaohongshu project."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from validate_project import load_and_validate

STYLE_LOCK = (
    "暖米白纸张质感背景；固定的呆萌眼镜漫画主持人：短黑发、透明灰色矩形眼镜、"
    "深灰圆领卫衣、黑色长裤、白色运动鞋，头大身小但不是火柴人；干净黑色描边和"
    "轻柔平涂；超大黑色手写感标题；钴蓝色笔刷、箭头、下划线和编号块；少量浅蓝"
    "圆角卡片；仅在语义图标上使用少量暖黄色；大量留白；适合小红书快速滑阅；"
    "人物身份、发型、眼镜、服装和比例跨页完全一致。"
)

NEGATIVE = (
    "不要写实摄影，不要3D，不要火柴人，不要赛博朋克，不要复杂背景，不要多色渐变，"
    "不要企业仪表盘，不要长段落，不要小字号，不要错误中文，不要错误英文产品名，"
    "不要乱码代码，不要多余水印，不要裁切标题、人物头部或底部总结。"
)


def quote_lines(lines: list[str]) -> str:
    return "\n".join(f"- {line}" for line in lines if line)


def cover_prompt(project: dict[str, Any]) -> str:
    cover = project["cover"]
    width = cover.get("width", 1080)
    height = cover.get("height", 1440)
    exact = [cover["title"], cover.get("subtitle", ""), cover.get("bottom_takeaway", "")]
    return f"""# 00 Cover — 3:4

生成一张竖版 3:4 小红书漫画图文封面，输出 {width}×{height}。

## Topic
{project['topic']}

## Audience
{project['audience']}

## Exact copy
{quote_lines(exact)}

## Composition
{cover['composition']}

## Character
{project['character']}

## Style lock
{STYLE_LOCK}

## Negative constraints
{NEGATIVE}

确保封面在缩略图尺寸下仍能读清主题。不要把内页的全部知识点塞进封面。
"""


def page_prompt(project: dict[str, Any], page: dict[str, Any]) -> str:
    width = page.get("width", 1080)
    height = page.get("height", 1920)
    exact = [page["title"], page["key_message"], *page.get("copy", [])]
    return f"""# {page['number']:02d} {page['title']} — 9:16

生成一张竖版 9:16 小红书漫画科普信息图，输出 {width}×{height}。一页只解释一个核心概念。

## Page role
- Archetype: {page['archetype']}
- Key message: {page['key_message']}

## Exact copy
{quote_lines(exact)}

## Visual narrative
{page['visual']}

## Character pose
{page['character_pose']}

## Diagram and reading flow
{page['flow']}

## Character
{project['character']}

## Style lock
{STYLE_LOCK}

## Negative constraints
{NEGATIVE}

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
