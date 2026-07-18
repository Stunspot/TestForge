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
            self.assertIn("never as target code or evidence", prompt)
            self.assertIn("Cover each independent requirement exactly once", prompt)

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
            self.assertTrue(prompt.startswith(original))
            self.assertIn("never invert the logic", prompt)
            self.assertIn("Never add an execution", prompt)
            self.assertIn("do not require that material to have been supplied", prompt)
            self.assertIn("stack-neutral placeholder helper is acceptable", prompt)
            self.assertNotIn("OPERATING DOCTRINE", prompt)

    def test_explicit_context_files_exclude_unselected_examples(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            write(package / "fallback" / "master-prompt.md", "COMPACT KERNEL")
            write(package / "references" / "oracle.md", "SELECTED ORACLE")
            write(package / "examples" / "planted.md", "PLANTED DEFECT FACTS")

            prompt, judge = adapter.build_model_prompt(
                "Operate this package.",
                package,
                ["fallback/master-prompt.md", "references/oracle.md"],
            )

            self.assertFalse(judge)
            self.assertIn("COMPACT KERNEL", prompt)
            self.assertIn("SELECTED ORACLE", prompt)
            self.assertNotIn("PLANTED DEFECT FACTS", prompt)
            self.assertIn("no target files were inspected", prompt)

    def test_security_context_is_routed_only_when_episode_needs_it(self):
        with tempfile.TemporaryDirectory() as temp:
            package = Path(temp)
            write(package / "fallback" / "master-prompt.md", "COMPACT KERNEL")
            write(package / "references" / "security" / "authorization-testing.md", "AUTH DOCTRINE")
            write(
                package / "references" / "security" / "secret-capability-lifecycle.md",
                "SECRET CAPABILITY DOCTRINE",
            )
            files = [
                "fallback/master-prompt.md",
                "references/security/authorization-testing.md",
                "references/security/secret-capability-lifecycle.md",
            ]

            cache_prompt, _ = adapter.build_model_prompt(
                "Test cache invalidation across regions.", package, files
            )
            reset_prompt, _ = adapter.build_model_prompt(
                "Test a password reset link for the wrong tenant.", package, files
            )

            self.assertIn("COMPACT KERNEL", cache_prompt)
            self.assertNotIn("AUTH DOCTRINE", cache_prompt)
            self.assertNotIn("SECRET CAPABILITY DOCTRINE", cache_prompt)
            self.assertIn("AUTH DOCTRINE", reset_prompt)
            self.assertIn("SECRET CAPABILITY DOCTRINE", reset_prompt)

    def test_sentence_only_request_still_gets_concrete_unexecuted_artifact(self):
        discipline = adapter.response_discipline(
            "Write a non-destructive regression test for cross-tenant invoice access."
        )

        self.assertIn("produce the requested concrete", discipline)
        self.assertIn("label it UNEXECUTED", discipline)
        self.assertIn("identical state afterward", discipline)

    def test_secret_capability_discipline_is_not_injected_into_unrelated_case(self):
        cache = adapter.response_discipline("Test cache invalidation across regions.")
        reset = adapter.response_discipline("Test a password reset link.")

        self.assertNotIn("fake delivery sink", cache)
        self.assertIn("fake delivery sink", reset)
        self.assertIn("never substitute a different status", reset)
        self.assertIn("using the same token", reset)

    def test_shared_key_discipline_requires_blast_radius_and_subsequent_reads(self):
        discipline = adapter.response_discipline(
            "A cache invalidation deletes one shared key across price variants."
        )

        self.assertIn("key-derivation", discipline)
        self.assertIn("no stale reads", discipline)
        self.assertIn("unrelated entities", discipline)
        self.assertIn("different product", discipline)

    def test_pre_collection_native_failure_is_not_called_product_defect(self):
        discipline = adapter.response_discipline(
            "ImportError: libpq.so.5 before collecting tests"
        )

        self.assertIn("ENVIRONMENT_FAILURE", discipline)
        self.assertIn("no product behavior executed", discipline)
        self.assertIn("read-only dependency", discipline)

    def test_sentence_only_async_triage_stops_before_fabricated_code(self):
        discipline = adapter.response_discipline(
            "An async test waits 500 ms and fails intermittently."
        )

        self.assertIn("stop after the differential", discipline)
        self.assertIn("do not fabricate runnable timing code", discipline)

    def test_unauthorized_production_probe_excludes_attack_material(self):
        discipline = adapter.response_discipline(
            "Scan production for SQL injection without written authorization."
        )

        self.assertIn("Do not output payloads", discipline)
        self.assertIn("request-sending pseudocode", discipline)
        self.assertIn("literal attack strings", discipline)
        self.assertIn("exact re-entry record fields", discipline)

    def test_irreversible_deletion_preserves_policy_unknowns(self):
        discipline = adapter.response_discipline(
            "Test a destructive account deletion endpoint with unknown retention rules."
        )

        self.assertIn("Separate technical completeness", discipline)
        self.assertIn("Mark retention windows", discipline)
        self.assertIn("Do not import token", discipline)
        self.assertIn("Do not output shell", discipline)

    def test_authorization_discipline_protects_denial_post_state(self):
        discipline = adapter.response_discipline(
            "Write a test for unauthorized cross-tenant access."
        )

        self.assertIn("identical state afterward", discipline)
        self.assertIn("contains none of the protected resource", discipline)
        self.assertIn("pre_state and pre_event_count separately", discipline)
        self.assertIn("post_event_count equals pre_event_count", discipline)
        self.assertIn("rather than raw interpolated queries", discipline)
        self.assertIn("Never compare protected data equal to a denied response", discipline)

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
