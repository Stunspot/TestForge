from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.6"
RELEASE_DATE = "2026-08-12"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseIdentityTests(unittest.TestCase):
    def test_version_and_date_sources_agree(self) -> None:
        package = (ROOT / "testforge" / "package-manifest.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"version: {VERSION}\n", package)
        self.assertIn(f"release_date: {RELEASE_DATE}\n", package)

        rebuild = load_module(
            "rebuild_public_release", ROOT / "tools" / "rebuild_public_release.py"
        )
        builder = load_module(
            "build_public_release", ROOT / "tools" / "build_public_release.py"
        )
        script_text = (
            ROOT / "testforge" / "scripts" / "build_release_manifest.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(VERSION, rebuild.VERSION)
        self.assertEqual(RELEASE_DATE, rebuild.RELEASE_DATE)
        self.assertEqual(VERSION, builder.VERSION)
        self.assertEqual(RELEASE_DATE, builder.DATE)
        self.assertIn(f'default="{VERSION}"', script_text)
        self.assertIn(f'default="{RELEASE_DATE}"', script_text)
        validator = load_module(
            "validate_release_manifests",
            ROOT / "tools" / "validate_release_manifests.py",
        )
        self.assertIn("evaluation-results", rebuild.EXCLUDED)
        self.assertIn("evaluation-results", validator.EXCLUDED)

        for manifest in (
            ROOT / "release-manifest.json",
            ROOT / "testforge" / "release-manifest.json",
        ):
            value = json.loads(manifest.read_text(encoding="utf-8-sig"))
            self.assertEqual(VERSION, value["version"])
            self.assertEqual(RELEASE_DATE, value["release_date"])

    def test_metered_plan_contract_is_packaged_and_excludes_authority(self) -> None:
        skill = ROOT / "testforge" / "skills" / "software-verification"
        schema = json.loads(
            (
                skill
                / "assets"
                / "schemas"
                / "metered-verification-plan.schema.json"
            ).read_text(encoding="utf-8")
        )
        plan = json.loads(
            (
                skill
                / "assets"
                / "templates"
                / "metered-verification-plan.json"
            ).read_text(encoding="utf-8")
        )
        self.assertFalse(schema["additionalProperties"])
        self.assertNotIn("paid_overage_authorization", schema["properties"])
        self.assertNotIn("consumed_authorization_ids", schema["properties"])
        self.assertNotIn("paid_overage_authorization", plan)
        self.assertNotIn("consumed_authorization_ids", plan)


if __name__ == "__main__":
    unittest.main()
