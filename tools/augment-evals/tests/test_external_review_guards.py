import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("reviewed_harness", Path(__file__).parents[1] / "augment_eval.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)

class EvidenceGuardTests(unittest.TestCase):
    def test_blank_subject_never_reaches_judge(self):
        rubric = {"case_id": "B", "trial": 1, "suite": "fixture", "dimensions": ["honesty"]}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for response in ("", " \n\t"):
                with patch.object(harness, "invoke_adapter") as judge:
                    harness.adjudicate_episode(root, {}, rubric, response, {}, root, root)
                    judge.assert_not_called()
                result = json.loads((root / "result.json").read_text())
                self.assertEqual(result["verdict"], "INVALID")
                self.assertIsNone(result["score"])

    def test_timeout_partial_output_survives_both_capture_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adapter = {"command": ["fixture"], "timeout_seconds": 1}
            for stdout, stderr in ((b"partial stdout", b"partial stderr"), ("partial stdout", "partial stderr"), (None, None)):
                for role in ("subject", "judge"):
                    with patch.object(harness.subprocess, "run", side_effect=subprocess.TimeoutExpired("fixture", 1, output=stdout, stderr=stderr)):
                        result = harness.invoke_adapter(adapter, "prompt", root, root, root, "B")
                    self.assertEqual(result["status"], "interrupted")
                    for field in ("stdout", "stderr"):
                        self.assertIsInstance(result[field], str)
                        target = root / (role + "-" + field + ".txt")
                        target.write_text(result[field], encoding="utf-8")
                        self.assertEqual(target.read_text(encoding="utf-8"), result[field])
                    self.assertEqual(result["stdout"], "" if stdout is None else "partial stdout")
                    self.assertEqual(result["stderr"], "" if stderr is None else "partial stderr")

class ExecutionPathTests(unittest.TestCase):
    def test_subject_and_judge_timeouts_preserve_partial_evidence_and_continue(self):
        from test_augment_eval import make_testforge_package, make_adapter
        for role in ("subject", "judge"):
            with self.subTest(role=role), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                package = make_testforge_package(root)
                adapter = make_adapter(root)
                suite = harness.load_eval_suite(package)
                run = harness.create_run(suite, root / "results", 2, "fixture", "fixture", str(adapter), str(adapter))
                calls = []
                def execute(command, **kwargs):
                    calls.append(kwargs["input"])
                    if role == "subject" or "EXPECTED BEHAVIORS" in kwargs["input"]:
                        raise subprocess.TimeoutExpired(command, 1, output=b"partial output", stderr=b"partial error")
                    return subprocess.CompletedProcess(command, 0, stdout="A real nonblank subject response", stderr="")
                with patch.object(harness.subprocess, "run", side_effect=execute):
                    harness.execute_run(run, adapter, adapter)
                self.assertEqual(harness.read_json(run / "run.json")["status"], "EXECUTED")
                episodes = list((run / "episodes").glob("*/trial-*"))
                self.assertEqual(len(episodes), 2)
                for episode in episodes:
                    self.assertEqual(harness.read_json(episode / "result.json")["verdict"], "INVALID")
                    execution = harness.read_json(episode / (role + "-execution.json"))
                    self.assertEqual(execution["stdout"], "partial output")
                    self.assertEqual(execution["stderr"], "partial error")
                    response = episode / ("subject-response.md" if role == "subject" else "judge-response.txt")
                    self.assertEqual(response.read_text(), "partial output")
                self.assertEqual(len(calls), 2 if role == "subject" else 4)

    def test_noop_and_partial_rejudging_keep_actual_evaluator_identity(self):
        from test_augment_eval import make_testforge_package, make_adapter
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = make_testforge_package(root)
            adapter = make_adapter(root)
            suite = harness.load_eval_suite(package)
            run = harness.create_run(suite, root / "results", 2, "fixture", "fixture", str(adapter), str(adapter))
            harness.execute_run(run, adapter, adapter)
            first = harness.summarize_run(run, append_ledger=False)["comparison_identity"]
            before = (run / "run.json").read_bytes()
            second_adapter = root / "second-adapter.json"
            config = harness.read_json(adapter)
            config["name"] = "second-judge"
            harness.write_json(second_adapter, config)
            self.assertEqual(harness.judge_prepared_run(run, second_adapter), 0)
            self.assertEqual((run / "run.json").read_bytes(), before)
            self.assertEqual(harness.summarize_run(run, append_ledger=False)["comparison_identity"], first)
            episodes = sorted((run / "episodes").glob("*/trial-*"))
            old_execution = (episodes[1] / "judge-execution.json").read_bytes()
            (episodes[0] / "result.json").unlink()
            self.assertEqual(harness.judge_prepared_run(run, second_adapter), 1)
            mixed = harness.summarize_run(run, append_ledger=False)["comparison_identity"]
            self.assertNotEqual(first["judge_adapter"], mixed["judge_adapter"])
            self.assertEqual((episodes[1] / "judge-execution.json").read_bytes(), old_execution)
            self.assertEqual(harness.read_json(episodes[0] / "judge-execution.json")["adapter_provenance"]["config_sha256"], harness.file_sha256(second_adapter))
            self.assertEqual(harness.read_json(episodes[1] / "judge-execution.json")["adapter_provenance"]["config_sha256"], harness.file_sha256(adapter))

    def test_comparison_identity_reads_actual_episode_rubric(self):
        from test_augment_eval import make_testforge_package, make_adapter
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = make_testforge_package(root)
            adapter = make_adapter(root)
            suite = harness.load_eval_suite(package)
            run = harness.create_run(suite, root / "results", 1, "fixture", "fixture", str(adapter), str(adapter))
            first = harness.summarize_run(run, append_ledger=False)["comparison_identity"]
            path = next((run / "episodes").glob("*/trial-*/evaluator-rubric.json"))
            rubric = harness.read_json(path)
            rubric["criteria"] = ["Changed real evaluator criterion"]
            harness.write_json(path, rubric)
            second = harness.summarize_run(run, append_ledger=False)["comparison_identity"]
            self.assertNotEqual(first["cases"], second["cases"])
            self.assertEqual(first["subject_adapter"], second["subject_adapter"])


class ComparisonGuardTests(unittest.TestCase):
    def summary(self):
        return {"run_id": "run", "mean_score": 100, "demonstrated_rate": 1,
                "verdicts": {"invalid": 0}, "claim_status": "DEMONSTRATED",
                "package_fingerprint_sha256": "old", "indispensable_gates": {"honesty": "PASSED"},
                "evaluated_episodes": 2, "expected_episodes": 2, "run_status": "COMPLETE",
                "comparison_identity": {"schema": "testforge-comparison-identity/v1", "cases": {"A": "rubric-a", "B": "rubric-b"}, "evaluator": "judge", "host": "host", "model": "model", "subject_adapter": "subject", "judge_adapter": "judge", "trials": 1}}

    def test_matching_identity_accepts_package_revision_and_rejects_score_drop(self):
        old, new = self.summary(), self.summary()
        new["package_fingerprint_sha256"] = "new"
        self.assertTrue(harness.check_regression(old, new, 0, 0, 0)["passed"])
        new["mean_score"] = 90
        self.assertFalse(harness.check_regression(old, new, 0, 0, 0)["passed"])

    def test_scope_and_execution_changes_need_reason_and_lose_baseline_significance(self):
        for key, value in (("cases", {"A": "rubric-a"}), ("cases", {"A": "changed", "B": "rubric-b"}), ("evaluator", "changed"), ("host", "changed"), ("model", "changed"), ("subject_adapter", "changed"), ("judge_adapter", "changed"), ("trials", 2)):
            old, new = self.summary(), self.summary()
            new["comparison_identity"][key] = value
            self.assertFalse(harness.check_regression(old, new, 0, 0, 0)["passed"])
            result = harness.check_regression(old, new, 0, 0, 0, comparison_change="intentional scoped comparison")
            self.assertTrue(result["passed"])
            self.assertFalse(result["comparison"]["full_baseline_comparable"])
            self.assertIsNone(result["comparison"]["mean_score_delta"])
            self.assertEqual(result["comparison"]["indispensable_gates"], {})

    def test_missing_identity_cannot_be_waived(self):
        old, new = self.summary(), self.summary()
        del new["comparison_identity"]
        self.assertFalse(harness.check_regression(old, new, 0, 0, 0, comparison_change="legacy") ["passed"])

    def test_codex_isolated_profile_never_launches_without_boundary(self):
        spec = importlib.util.spec_from_file_location("codex_guard", Path(__file__).parents[1] / "adapters/codex_cli_adapter.py")
        adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(adapter)
        with patch.object(adapter.subprocess, "run") as launch:
            self.assertEqual(adapter.main(["--require-evaluator-isolation", "exec", "-"]), 2)
            launch.assert_not_called()

if __name__ == "__main__":
    unittest.main()
