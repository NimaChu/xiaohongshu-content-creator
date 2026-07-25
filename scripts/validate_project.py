#!/usr/bin/env python3
"""Validate a Xiaohongshu Content Creator project JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_TOP = {"topic", "audience", "thesis", "character", "cover", "pages"}
REQUIRED_COVER = {"title", "composition"}
REQUIRED_PAGE = {
    "number",
    "title",
    "archetype",
    "key_message",
    "visual",
    "character_pose",
    "flow",
}
SUPPORTED_LOCAL_KINDS = {
    "article_page",
    "mechanism",
    "checklist",
    "qa",
    "catalog",
    "map",
    "comparison",
    "flow",
    "timeline",
    "article_note",
}


def text_len(value: Any) -> int:
    return len(str(value).strip())


def close_ratio(width: int, height: int, expected: float, tolerance: float = 0.015) -> bool:
    return abs((width / height) - expected) <= tolerance


def _validate_dimensions(
    errors: list[str],
    where: str,
    value: dict[str, Any],
    default_width: int,
    default_height: int,
    expected_ratio: float,
) -> None:
    width = value.get("width", default_width)
    height = value.get("height", default_height)
    if not isinstance(width, int) or not isinstance(height, int) or width < 320 or height < 320:
        errors.append(f"{where} width and height must be integers of at least 320")
        return
    if not close_ratio(width, height, expected_ratio):
        errors.append(f"{where} must use a {expected_ratio:.4f} aspect ratio; got {width}x{height}")


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["Project JSON must contain an object at the top level"]

    missing = REQUIRED_TOP - data.keys()
    if missing:
        errors.append(f"Missing top-level fields: {sorted(missing)}")
        return errors

    for field in ("topic", "audience", "thesis", "character"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")

    cover = data["cover"]
    if not isinstance(cover, dict):
        errors.append("cover must be an object")
    else:
        missing_cover = REQUIRED_COVER - cover.keys()
        if missing_cover:
            errors.append(f"Missing cover fields: {sorted(missing_cover)}")
        if text_len(cover.get("title", "")) > 30:
            errors.append("Cover title is too long; keep it under 30 characters")
        _validate_dimensions(errors, "cover", cover, 1080, 1440, 3 / 4)

    pages = data["pages"]
    if not isinstance(pages, list):
        errors.append("pages must be a list")
        return errors
    if not 4 <= len(pages) <= 10:
        errors.append("Use 4–10 information pages")

    numbers: list[int] = []
    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            errors.append(f"Page {index} must be an object")
            continue
        missing_page = REQUIRED_PAGE - page.keys()
        if missing_page:
            errors.append(f"Page {index} missing fields: {sorted(missing_page)}")
        number = page.get("number")
        if isinstance(number, int):
            numbers.append(number)
        else:
            errors.append(f"Page {index} number must be an integer")
        if text_len(page.get("title", "")) > 24:
            errors.append(f"Page {index} title is too long")
        copy = page.get("copy", [])
        if not isinstance(copy, list) or any(not isinstance(item, str) for item in copy):
            errors.append(f"Page {index} copy must be a list of strings")
        elif len(copy) > 8:
            errors.append(f"Page {index} has too many copy items; keep 8 or fewer")
        elif sum(text_len(item) for item in copy) > 180:
            errors.append(f"Page {index} has too much supporting copy (>180 characters)")
        local_kind = page.get("local_kind")
        if local_kind is not None and local_kind not in SUPPORTED_LOCAL_KINDS:
            errors.append(
                f"Page {index} local_kind must be one of: {', '.join(sorted(SUPPORTED_LOCAL_KINDS))}"
            )
        _validate_dimensions(errors, f"Page {index}", page, 1080, 1920, 9 / 16)

    if numbers and numbers != list(range(1, len(numbers) + 1)):
        errors.append("Page numbers must be sequential starting at 1")

    post = data.get("post")
    if post is not None and not isinstance(post, dict):
        errors.append("post must be an object when provided")
    elif isinstance(post, dict):
        hashtags = post.get("hashtags", [])
        if not isinstance(hashtags, list) or any(not isinstance(item, str) for item in hashtags):
            errors.append("post.hashtags must be a list of strings")

    return errors


def load_and_validate(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        raise ValueError("\n".join(errors))
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args()

    try:
        load_and_validate(args.project)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        for line in str(exc).splitlines():
            print(f"ERROR: {line}")
        return 1
    print(f"OK: {args.project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
