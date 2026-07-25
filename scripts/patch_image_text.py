#!/usr/bin/env python3
"""Overlay corrected text on one explicit rectangular region of a PNG."""

from __future__ import annotations

import argparse
import base64
import html
import tempfile
from pathlib import Path

from check_png_ratios import png_size
from free_image_gen import export_svg_to_png


def wrap_text(text: str, max_units: int) -> list[str]:
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        current = ""
        units = 0
        for character in paragraph:
            character_units = 1 if ord(character) > 127 else 0.55
            if current and units + character_units > max_units:
                lines.append(current)
                current = character
                units = character_units
            else:
                current += character
                units += character_units
        lines.append(current)
    return lines or [""]


def build_patch_svg(
    input_path: Path,
    canvas_width: int,
    canvas_height: int,
    x: int,
    y: int,
    region_width: int,
    region_height: int,
    text: str,
    font_size: int,
    background: str,
    foreground: str,
    align: str,
    radius: int,
) -> str:
    encoded = base64.b64encode(input_path.read_bytes()).decode("ascii")
    max_units = max(1, int((region_width - font_size) / font_size))
    lines = wrap_text(text, max_units)
    line_height = font_size * 1.25
    total_height = line_height * len(lines)
    start_y = y + max(font_size, (region_height - total_height) / 2 + font_size)
    if align == "center":
        text_x = x + region_width / 2
        anchor = "middle"
    else:
        text_x = x + font_size * 0.5
        anchor = "start"
    tspans = "".join(
        f'<tspan x="{text_x:.2f}" y="{start_y + index * line_height:.2f}">{html.escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}">
  <image href="data:image/png;base64,{encoded}" x="0" y="0" width="{canvas_width}" height="{canvas_height}"/>
  <rect x="{x}" y="{y}" width="{region_width}" height="{region_height}" rx="{radius}" fill="{html.escape(background)}"/>
  <text x="{text_x:.2f}" y="{start_y:.2f}" text-anchor="{anchor}" font-family="PingFang SC, Hiragino Sans GB, Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="{font_size}" font-weight="800" fill="{html.escape(foreground)}">{tspans}</text>
</svg>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--x", type=int, required=True)
    parser.add_argument("--y", type=int, required=True)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--font-size", type=int, default=72)
    parser.add_argument("--background", default="#F6F3ED")
    parser.add_argument("--foreground", default="#101010")
    parser.add_argument("--align", choices=["left", "center"], default="center")
    parser.add_argument("--radius", type=int, default=18)
    args = parser.parse_args()

    try:
        input_path = args.input.expanduser().resolve()
        output_path = args.output.expanduser().resolve()
        if input_path == output_path:
            raise ValueError("Refusing to overwrite the source image; choose a different --output path")
        canvas_width, canvas_height = png_size(input_path)
        if args.width <= 0 or args.height <= 0:
            raise ValueError("Patch width and height must be positive")
        if args.x < 0 or args.y < 0 or args.x + args.width > canvas_width or args.y + args.height > canvas_height:
            raise ValueError("Patch region must stay inside the source image")

        svg = build_patch_svg(
            input_path,
            canvas_width,
            canvas_height,
            args.x,
            args.y,
            args.width,
            args.height,
            args.text,
            args.font_size,
            args.background,
            args.foreground,
            args.align,
            args.radius,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="xhs-text-patch-") as tmpdir:
            svg_path = Path(tmpdir) / "patch.svg"
            svg_path.write_text(svg, encoding="utf-8")
            export_svg_to_png(svg_path, output_path, canvas_width, canvas_height)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
