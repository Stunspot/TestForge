from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "adapters" / "ollama_context_adapter.py"
SPEC = importlib.util.spec_from_file_location("ollama_context_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class ContextCustodyTests(unittest.TestCase):
    def test_subject_bundle_includes_operating_material_but_excludes_evals(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            write(package / "skills" / "operator" / "SKILL.md", "OPERATING DOCTRINE")
            write(package / "references" / "oracle.md", "ORACLE REFERENCE")
            write(package / "evals" / "cases.yaml", "SECRET ANSWER KEY")

            prompt, judge = adapter.build_model_prompt("Operate this package.", package)

            self.assertFalse(judge)
            self.assertIn("OPERATING DOCTRINE", prompt)
            self.assertIn("ORACLE REFERENCE", prompt)
            self.assertNotIn("SECRET ANSWER KEY", prompt)
            self.assertNotIn("evals/cases.yaml", prompt)
            self.assertNotIn("evaluation suite", prompt.lower())
            self.assertNotIn("answer key", prompt.lower())
            self.assertIn("not as something to discuss with the user", prompt)

    def test_root_installed_skill_bundle_includes_connected_runtime_material(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            write(package / "SKILL.md", "ROOT OPERATING SKILL")
            write(package / "personas" / "specialist.md", "SPECIALIST PERSONA")
            write(package / "workflows" / "incident.md", "INCIDENT WORKFLOW")
            write(package / "assets" / "incident-report.md", "INCIDENT TEMPLATE")
            write(package / "schemas" / "incident.json", '{"title": "INCIDENT SCHEMA"}')
            write(package / "examples" / "handoff.md", "HANDOFF DEMONSTRATION")
            write(package / "scripts" / "unsafe-to-assume-loaded.py", "SCRIPT CONTENT")
            write(package / "evals" / "cases.yaml", "SECRET ROOT-SKILL RUBRIC")

            context = adapter.collect_package_context(package)

            self.assertIn("ROOT OPERATING SKILL", context)
            self.assertIn("SPECIALIST PERSONA", context)
            self.assertIn("INCIDENT WORKFLOW", context)
            self.assertIn("INCIDENT TEMPLATE", context)
            self.assertIn("INCIDENT SCHEMA", context)
            self.assertIn("HANDOFF DEMONSTRATION", context)
            self.assertNotIn("SCRIPT CONTENT", context)
            self.assertNotIn("SECRET ROOT-SKILL RUBRIC", context)
            self.assertLess(context.index("ROOT OPERATING SKILL"), context.index("SPECIALIST PERSONA"))
            self.assertLess(context.index("SPECIALIST PERSONA"), context.index("INCIDENT WORKFLOW"))

    def test_judge_prompt_is_not_augmented_with_package_material(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            write(package / "skills" / "operator" / "SKILL.md", "OPERATING DOCTRINE")
            original = adapter.JUDGE_PREFIX + " against the rubric."

            prompt, judge = adapter.build_model_prompt(original, package)

            self.assertTrue(judge)
            self.assertEqual(original, prompt)
            self.assertNotIn("OPERATING DOCTRINE", prompt)

    def test_reasoning_mode_is_forwarded_to_ollama(self):
        response = io.BytesIO(json.dumps({"response": "visible output"}).encode("utf-8"))
        with patch.object(adapter.urllib.request, "urlopen", return_value=response) as mocked:
            output = adapter.invoke_ollama(
                "http://127.0.0.1:11434",
                "qwen35",
                "prompt",
                False,
                65536,
                30,
                False,
            )

        payload = json.loads(mocked.call_args.args[0].data.decode("utf-8"))
        self.assertEqual("visible output", output)
        self.assertIs(payload["think"], False)

    def test_cpu_only_mode_is_forwarded_to_ollama(self):
        response = io.BytesIO(json.dumps({"response": "visible output"}).encode("utf-8"))
        with patch.object(adapter.urllib.request, "urlopen", return_value=response) as mocked:
            adapter.invoke_ollama(
                "http://127.0.0.1:11434",
                "qwen35",
                "prompt",
                False,
                32768,
                30,
                False,
                0,
            )

        payload = json.loads(mocked.call_args.args[0].data.decode("utf-8"))
        self.assertEqual(0, payload["options"]["num_gpu"])


if __name__ == "__main__":
    unittest.main()
