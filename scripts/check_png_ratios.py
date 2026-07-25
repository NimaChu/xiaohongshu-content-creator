#!/usr/bin/env python3
"""Check that cover.png is 3:4 and page-*.png files are 9:16."""

from __future__ import annotations

import argparse
import struct
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as file:
        if file.read(8) != PNG_SIGNATURE:
            raise ValueError("not a PNG file")
        length = struct.unpack(">I", file.read(4))[0]
        chunk_type = file.read(4)
        if chunk_type != b"IHDR" or length < 8:
            raise ValueError("missing PNG IHDR")
        return struct.unpack(">II", file.read(8))


def close_ratio(width: int, height: int, expected: float, tolerance: float) -> bool:
    return abs((width / height) - expected) <= tolerance


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--tolerance", type=float, default=0.015)
    args = parser.parse_args()

    failures = 0
    cover = args.directory / "cover.png"
    pages = sorted(args.directory.glob("page-*.png"))
    if not cover.exists():
        print("ERROR: cover.png is missing")
        failures += 1
    if not pages:
        print("ERROR: no page-*.png files found")
        failures += 1

    for path in [cover, *pages]:
        if not path.exists():
            continue
        try:
            width, height = png_size(path)
        except ValueError as exc:
            print(f"ERROR: {path.name}: {exc}")
            failures += 1
            continue
        expected = 3 / 4 if path.name == "cover.png" else 9 / 16
        ok = close_ratio(width, height, expected, args.tolerance)
        print(f"{'OK' if ok else 'ERROR'}: {path.name}: {width}x{height}")
        failures += 0 if ok else 1

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
