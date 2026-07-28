from __future__ import annotations

import json
import struct
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_png_ratios import png_size
from make_prompt_pack import cover_prompt, page_prompt
from patch_image_text import build_patch_svg, resolve_patch_background
from render_xiaohongshu_project import build_render_plan, infer_local_kind, local_copy_for_kind
from validate_project import validate


class ProjectToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project = json.loads(
            (ROOT / "references" / "project.template.json").read_text(encoding="utf-8")
        )

    def test_template_project_is_valid(self) -> None:
        self.assertEqual(validate(self.project), [])

    def test_validator_rejects_wrong_ratios_and_too_few_pages(self) -> None:
        project = deepcopy(self.project)
        project["cover"]["height"] = 1920
        project["pages"] = project["pages"][:2]
        errors = validate(project)
        self.assertTrue(any("3:4" in error or "0.7500" in error for error in errors))
        self.assertIn("Use 4–10 information pages", errors)

    def test_validator_requires_anchor_metaphor_and_core_character_action(self) -> None:
        project = deepcopy(self.project)
        project["pages"][0].pop("cognitive_anchor")
        project["pages"][1]["metaphor"]["physical_action"] = ""
        project["pages"][2]["character_action"] = ""
        errors = validate(project)
        self.assertTrue(any("cognitive_anchor" in error for error in errors))
        self.assertTrue(any("metaphor.physical_action" in error for error in errors))
        self.assertTrue(any("character_action" in error for error in errors))

    def test_validator_rejects_unknown_visual_profile(self) -> None:
        project = deepcopy(self.project)
        project["visual_profile"] = "future-profile-not-registered"
        errors = validate(project)
        self.assertTrue(any("Unknown visual_profile" in error for error in errors))

    def test_render_plan_uses_mixed_xiaohongshu_ratios(self) -> None:
        plan = build_render_plan(self.project)
        self.assertEqual(plan[0]["filename"], "cover.png")
        self.assertEqual((plan[0]["width"], plan[0]["height"]), (1080, 1440))
        self.assertEqual(plan[1]["filename"], "page-01.png")
        self.assertEqual((plan[1]["width"], plan[1]["height"]), (1080, 1920))
        self.assertEqual(len(plan), len(self.project["pages"]) + 1)
        self.assertIn("标题：终端", plan[0]["prompt"])
        self.assertIn("给小白讲清楚", plan[0]["prompt"])

    def test_explicit_and_inferred_local_kinds(self) -> None:
        self.assertEqual(infer_local_kind(self.project["pages"][0]), "comparison")
        page = deepcopy(self.project["pages"][0])
        page.pop("local_kind")
        page["archetype"] = "capability grid"
        self.assertEqual(infer_local_kind(page), "catalog")

    def test_comparison_copy_is_structured_for_local_renderer(self) -> None:
        rows = local_copy_for_kind(
            "comparison",
            ["以前：用鼠标点点点", "现在：用命令让电脑做事", "更高效"],
        )
        self.assertEqual(rows[0], "操作方式：用鼠标点点点 / 用命令让电脑做事")
        self.assertEqual(rows[1], "结论： / 更高效")

    def test_image_prompts_contain_fixed_ratios_and_exact_copy(self) -> None:
        cover = cover_prompt(self.project)
        page = page_prompt(self.project, self.project["pages"][0])
        self.assertIn("3:4", cover)
        self.assertIn("1080×1440", cover)
        self.assertIn(self.project["cover"]["title"], cover)
        self.assertIn("9:16", page)
        self.assertIn("1080×1920", page)
        self.assertIn(self.project["pages"][0]["key_message"], page)
        self.assertIn("Cognitive anchor", page)
        self.assertIn("Original visual metaphor", page)
        self.assertIn(self.project["pages"][0]["character_action"], page)
        self.assertIn("alpaca-line-art", page)
        self.assertIn(
            "assets/characters/alpaca-line-art/character-sheet.png",
            page,
        )
        self.assertIn("纯白背景", page)

    def test_prompt_pack_can_select_legacy_visual_profile(self) -> None:
        project = deepcopy(self.project)
        project["visual_profile"] = "glasses-chibi-blue"
        page = page_prompt(project, project["pages"][0])
        self.assertIn("glasses-chibi-blue", page)
        self.assertIn(
            "assets/characters/glasses-chibi-blue/character-sheet.png",
            page,
        )
        self.assertIn("暖米白纸张质感背景", page)
        self.assertNotIn("白色羊驼", page)

    def test_all_visual_profiles_are_registered_and_usable(self) -> None:
        registry = json.loads(
            (ROOT / "references" / "visual-profiles.json").read_text(encoding="utf-8")
        )
        expected = {
            "alpaca-line-art",
            "glasses-chibi-blue",
            "toolbox-bot-risograph",
            "maker-girl-editorial",
            "cyber-luban-woodcut",
            "capybara-gouache",
        }
        self.assertEqual(set(registry["profiles"]), expected)

        for profile_id in expected:
            profile = registry["profiles"][profile_id]
            self.assertTrue((ROOT / profile["character_reference"]).is_file())
            project = deepcopy(self.project)
            project["visual_profile"] = profile_id
            prompt = page_prompt(project, project["pages"][0])
            self.assertIn(profile_id, prompt)
            self.assertIn(profile["character_reference"], prompt)

    def test_image_prompts_forbid_page_position_markers(self) -> None:
        page = page_prompt(self.project, self.project["pages"][0])
        self.assertIn("禁止显示任何页码、总页数或分页位置标记", page)
        self.assertNotIn("角标：", build_render_plan(self.project)[1]["prompt"])

    def test_png_header_reader(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test.png"
            path.write_bytes(
                b"\x89PNG\r\n\x1a\n"
                + struct.pack(">I", 13)
                + b"IHDR"
                + struct.pack(">II", 1080, 1440)
                + b"\x08\x06\x00\x00\x00"
            )
            self.assertEqual(png_size(path), (1080, 1440))

    def test_text_patch_svg_embeds_source_and_escapes_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.png"
            source.write_bytes(b"fake-png-data")
            svg = build_patch_svg(
                source,
                1080,
                1920,
                100,
                200,
                800,
                180,
                "正确文字 & AI",
                72,
                "#FFFFFF",
                "#101010",
                "center",
                18,
            )
            self.assertIn("data:image/png;base64", svg)
            self.assertIn("正确文字 &amp; AI", svg)
            self.assertIn('x="100"', svg)

    def test_text_patch_uses_selected_profile_background(self) -> None:
        self.assertEqual(resolve_patch_background(None, "alpaca-line-art"), "#FFFFFF")
        self.assertEqual(
            resolve_patch_background(None, "glasses-chibi-blue"),
            "#F6F3ED",
        )
        self.assertEqual(
            resolve_patch_background("#ABCDEF", "glasses-chibi-blue"),
            "#ABCDEF",
        )


if __name__ == "__main__":
    unittest.main()
