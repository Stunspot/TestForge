from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPTS = PACKAGE / "scripts"
sys.path.insert(0, str(SCRIPTS))

from assemble_report import assemble
from detect_test_stack import detect
from inspect_repo import inspect
from normalize_test_results import normalize
from scan_test_smells import scan
from validate_manifest import validate as validate_manifest
from validate_traceability import validate as validate_traceability
from verify_package import verify as verify_package


def base_manifest() -> dict:
    return {
        "manifest_version": "1.0",
        "target": {"name": "fixture", "revision": "abc", "target_class": "change"},
        "scope": {"included": ["behavior"], "excluded": [], "constraints": [], "safety_boundary": ["local"]},
        "claim_custody": {"observed": [], "inferred": [], "assumed": [], "unresolved": []},
        "invariants": [{"id": "INV-001", "statement": "behavior remains true"}],
        "risks": [], "scenarios": [], "tests": [], "executions": [], "findings": [], "residual_risks": [],
        "review": {"status": "REVIEW_PASS", "findings": []},
        "decision": {"status": "READY", "basis": ["fixture"], "authority_required": []},
    }


class ToolTests(unittest.TestCase):
    def test_vitest_signal_does_not_imply_playwright(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "package.json").write_text(json.dumps({"scripts": {"test": "vitest run"}, "devDependencies": {"vitest": "2"}}), encoding="utf-8")
            frameworks = [item["framework"] for item in detect(root)["candidates"]]
            self.assertEqual(["vitest"], frameworks)

    def test_nested_unittest_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); nested = root / "example" / "expected"; nested.mkdir(parents=True)
            (nested / "test_behavior.py").write_text("import unittest\nclass T(unittest.TestCase):\n    pass\n", encoding="utf-8")
            frameworks = [item["framework"] for item in detect(root)["candidates"]]
            self.assertEqual(["unittest"], frameworks)

    def test_inspector_ignores_dependency_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / "tests").mkdir(); (root / "node_modules").mkdir()
            (root / "tests" / "test_unit.py").write_text("assert True\n", encoding="utf-8")
            (root / "node_modules" / "hidden.py").write_text("", encoding="utf-8")
            result = inspect(root)
            self.assertEqual(1, result["file_count"])
            self.assertEqual(1, result["test_file_count"])

    def test_ready_rejects_unresolved_critical_risk(self):
        data = base_manifest()
        data["risks"] = [{"id": "R-001", "statement": "critical", "severity": "critical", "disposition": "unresolved", "verification": ["S-X-001"]}]
        data["scenarios"] = [{"id": "S-X-001", "risk_ids": ["R-001"], "expected": ["safe"], "action": ["act"]}]
        report = validate_manifest(data)
        self.assertFalse(report["valid"])
        self.assertTrue(any("ready status conflicts" in error for error in report["errors"]))

    def test_covered_risk_requires_completed_execution(self):
        data = base_manifest(); data["decision"]["status"] = "BLOCKED_BY_ENVIRONMENT"
        data["risks"] = [{"id": "R-001", "statement": "risk", "severity": "critical", "disposition": "covered", "verification": ["S-X-001"]}]
        data["scenarios"] = [{"id": "S-X-001", "risk_ids": ["R-001"], "expected": ["safe"], "action": ["act"]}]
        report = validate_traceability(data)
        self.assertFalse(report["valid"])
        self.assertTrue(any("no test" in error for error in report["errors"]))

    def test_junit_normalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "junit.xml"
            path.write_text('<testsuite tests="2" failures="1"><testcase name="a"/><testcase name="b"><failure>bad</failure></testcase></testsuite>', encoding="utf-8")
            result = normalize(path)
            self.assertEqual({"total": 2, "passed": 1, "failed": 1, "skipped": 0, "errors": 0, "status": "failed"}, result["summary"])

    def test_smell_scan_is_explicitly_heuristic(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "test_wait.py"; path.write_text("def test_wait():\n    time.sleep(1)\n", encoding="utf-8")
            result = scan([path])
            self.assertTrue(result["heuristic_only"])
            self.assertGreaterEqual(result["finding_count"], 1)

    def test_report_refuses_placeholder(self):
        data = base_manifest(); data["target"]["name"] = "REPLACE"
        with self.assertRaises(ValueError):
            assemble(data)

    def test_package_verifier_detects_json_escaped_private_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "E:" + "\\" + "Github\\cd-augment-lab\\private.json"
            (root / "record.json").write_text(
                json.dumps({"path": private_path}),
                encoding="utf-8",
            )
            result = verify_package(root)
            self.assertIn(
                "private absolute path found in record.json",
                result["errors"],
            )


if __name__ == "__main__":
    unittest.main()
