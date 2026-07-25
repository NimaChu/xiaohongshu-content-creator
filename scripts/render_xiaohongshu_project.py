#!/usr/bin/env python3
"""Render a Xiaohongshu project locally with mixed cover and page ratios."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from free_image_gen import generate_image
from validate_project import load_and_validate

KIND_LABELS = {
    "article_page": "文章页",
    "mechanism": "机制卡",
    "checklist": "清单卡",
    "qa": "问答卡",
    "catalog": "目录卡",
    "map": "地图卡",
    "comparison": "对比卡",
    "flow": "流程卡",
    "timeline": "时间线卡",
    "article_note": "说明卡",
}


def infer_local_kind(page: dict[str, Any]) -> str:
    explicit = page.get("local_kind")
    if explicit:
        return explicit

    value = f"{page.get('archetype', '')} {page.get('title', '')}".lower()
    rules = [
        (("before", "after", "comparison", "对比", "以前", "现在"), "comparison"),
        (("timeline", "时间线", "历程"), "timeline"),
        (("workflow", "flow", "流程", "步骤"), "flow"),
        (("capability", "grid", "catalog", "能力", "盘点"), "catalog"),
        (("human-in-the-loop", "mechanism", "机制", "循环"), "mechanism"),
        (("qa", "问答", "为什么"), "qa"),
        (("summary", "checklist", "总结", "清单"), "checklist"),
    ]
    for tokens, kind in rules:
        if any(token in value for token in tokens):
            return kind
    return "article_page"


def _numbered_copy(items: list[str]) -> str:
    return " ".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def _without_prefix(value: str, prefixes: tuple[str, ...]) -> str:
    for prefix in prefixes:
        if value.startswith(prefix):
            return value[len(prefix):].lstrip("：: ").strip()
    return value.strip()


def local_copy_for_kind(kind: str, items: list[str]) -> list[str]:
    if kind != "comparison":
        return items

    before = next((item for item in items if item.startswith(("以前", "过去", "Before"))), None)
    after = next((item for item in items if item.startswith(("现在", "如今", "After"))), None)
    if before and after:
        rows = [
            "操作方式："
            + _without_prefix(before, ("以前", "过去", "Before"))
            + " / "
            + _without_prefix(after, ("现在", "如今", "After"))
        ]
        for item in items:
            if item not in {before, after}:
                rows.append(f"结论： / {item}")
        return rows

    return [f"要点{index}：{item} /" for index, item in enumerate(items, start=1)]


def build_cover_prompt(project: dict[str, Any]) -> str:
    cover = project["cover"]
    title = cover["title"]
    hook = ""
    for separator in ("：", ":"):
        if separator in title:
            hook, title = (part.strip() for part in title.split(separator, 1))
            break
    subtitle = cover.get("subtitle", "")
    takeaway = cover.get("bottom_takeaway", "")
    subtitle_line = "｜".join(value for value in (hook, subtitle, takeaway) if value)
    parts = [
        f"文字封面，标题：{title}",
        f"副标题：{subtitle_line}" if subtitle_line else "",
        "主题：light",
        "页面密度：comfy",
        "系列风格：unified",
        "页面角色：cover",
        "页面风格：soft",
        "强调色：blue",
        "语气：playful",
        "装饰密度：low",
        "表情策略：sparse",
        "封面布局：title_first",
    ]
    return "\n".join(part for part in parts if part)


def build_page_prompt(page: dict[str, Any]) -> str:
    kind = infer_local_kind(page)
    label = KIND_LABELS[kind]
    copy = [str(item).strip() for item in page.get("copy", []) if str(item).strip()]
    local_copy = local_copy_for_kind(kind, copy)
    parts = [
        f"信息图 {label}",
        f"角标：{page['number']:02d}",
        f"标题：{page['title']}",
        f"副标题：{page['key_message']}",
        _numbered_copy(local_copy),
        f"主题：{page.get('theme', 'light')}",
        f"页面密度：{page.get('density', 'comfy')}",
        "系列风格：unified",
        "页面角色：body",
        f"页面风格：{page.get('surface_style', 'soft')}",
        f"强调色：{page.get('accent', 'blue')}",
    ]
    return "\n".join(part for part in parts if part)


def build_render_plan(project: dict[str, Any]) -> list[dict[str, Any]]:
    cover = project["cover"]
    plan: list[dict[str, Any]] = [
        {
            "role": "cover",
            "filename": "cover.png",
            "prompt_filename": "00-cover.md",
            "width": cover.get("width", 1080),
            "height": cover.get("height", 1440),
            "prompt": build_cover_prompt(project),
        }
    ]
    for page in project["pages"]:
        number = page["number"]
        plan.append(
            {
                "role": "page",
                "number": number,
                "local_kind": infer_local_kind(page),
                "filename": f"page-{number:02d}.png",
                "prompt_filename": f"{number:02d}-page.md",
                "width": page.get("width", 1080),
                "height": page.get("height", 1920),
                "prompt": build_page_prompt(page),
            }
        )
    return plan


def render_project(
    project_path: Path,
    output_dir: Path,
    prompts_only: bool = False,
    keep_svg: bool = False,
) -> dict[str, Any]:
    project = load_and_validate(project_path)
    output_dir = output_dir.expanduser().resolve()
    images_dir = output_dir / "images"
    prompts_dir = output_dir / "prompts" / "local"
    images_dir.mkdir(parents=True, exist_ok=True)
    prompts_dir.mkdir(parents=True, exist_ok=True)

    target_project = output_dir / "project.json"
    if project_path.resolve() != target_project.resolve():
        shutil.copyfile(project_path, target_project)

    plan = build_render_plan(project)
    results: list[dict[str, Any]] = []
    for item in plan:
        prompt_path = prompts_dir / item["prompt_filename"]
        prompt_path.write_text(item["prompt"].rstrip() + "\n", encoding="utf-8")
        result = {
            "filename": item["filename"],
            "prompt": str(prompt_path),
            "width": item["width"],
            "height": item["height"],
            "local_kind": item.get("local_kind", "text_cover"),
        }
        if not prompts_only:
            png_path = images_dir / item["filename"]
            rendered = generate_image(
                item["prompt"],
                png_path,
                item["width"],
                item["height"],
                keep_svg=keep_svg,
            )
            result["png"] = rendered["png"]
            result["svg"] = rendered["svg"]
        results.append(result)

    manifest = {
        "mode": "xiaohongshu-local-fallback",
        "project": str(target_project),
        "images_dir": str(images_dir),
        "prompts_dir": str(prompts_dir),
        "generated_count": 0 if prompts_only else len(results),
        "items": results,
    }
    manifest_path = output_dir / "local-render.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--prompts-only", action="store_true")
    parser.add_argument("--keep-svg", action="store_true")
    args = parser.parse_args()

    try:
        result = render_project(
            args.project,
            args.output_dir,
            prompts_only=args.prompts_only,
            keep_svg=args.keep_svg,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
