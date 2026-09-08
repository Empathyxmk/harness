from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from migration_harness.core import (
    AgentTurn,
    Task,
    Usage,
    _parse_codex_jsonl,
    agent_change_stats,
    build_eval_workspace,
    dataset_root,
    normalised_rate,
    parse_test_output,
    prepare_workspace,
)


def _demo_dataset(root: Path) -> Task:
    src = root / "source_projects" / "Java" / "demo"
    tgt = root / "target_projects" / "Java" / "Python" / "demo"
    src.mkdir(parents=True)
    tgt.mkdir(parents=True)

    (src / "A.java").write_text("class A {}", encoding="utf-8")
    (tgt / "impl.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tgt / "public.py").write_text("PUBLIC = 1\n", encoding="utf-8")
    (tgt / "hidden.py").write_text("HIDDEN = 1\n", encoding="utf-8")
    (tgt / "run_tests.sh").write_text("exit 0\n", encoding="utf-8")

    meta = {
        "project_name": "demo",
        "source_language": "Java",
        "target_language": "Python",
        "target_public_tests": ["public.py"],
        "target_original_tests": ["hidden.py"],
        "run_tests_script": "run_tests.sh",
    }
    (root / "target_projects" / "projects_summary.jsonl").write_text(
        json.dumps(meta) + "\n", encoding="utf-8"
    )
    return Task(root, meta)


class ParserTests(unittest.TestCase):
    def test_pytest_parser(self):
        r = parse_test_output("8 passed, 2 failed in 1.0s", "", 1, 1.0)
        self.assertEqual(r.passed, 8)
        self.assertEqual(r.failed, 2)
        self.assertEqual(r.total, 10)
        self.assertAlmostEqual(r.pass_rate, 0.8)
        self.assertFalse(r.full_success)

    def test_unittest_parser(self):
        r = parse_test_output(
            "Ran 10 tests in 0.1s\nFAILED (failures=1, errors=2)", "", 1, 0.1
        )
        self.assertEqual(r.passed, 7)
        self.assertEqual(r.failed, 3)

    def test_parser_sums_multiple_pytest_invocations(self):
        """
        Several run_tests.sh scripts call pytest twice. Reading only the final
        summary block silently discards the first invocation.
        """
        out = "9 passed in 0.4s\n" "14 passed, 3 failed in 0.9s\n"
        r = parse_test_output(out, "", 1, 1.0)
        self.assertEqual(r.passed, 23)
        self.assertEqual(r.failed, 3)
        self.assertEqual(r.total, 26)

    def test_exit_code_fallback(self):
        r = parse_test_output("nothing recognisable", "", 0, 0.1)
        self.assertEqual(r.parser, "exit_code")
        self.assertIsNone(r.total)
        self.assertTrue(r.full_success)


class AgentHealthTests(unittest.TestCase):
    def test_quota_failure_is_detected_despite_clean_exit(self):
        """Codex reports quota exhaustion in the event stream, not the exit code."""
        stream = "\n".join([
            '{"type":"thread.started","thread_id":"abc"}',
            '{"type":"turn.started"}',
            '{"type":"error","message":"You\'ve hit your usage limit."}',
            '{"type":"turn.failed","error":{"message":"You\'ve hit your usage limit."}}',
        ])
        parsed = _parse_codex_jsonl(stream)
        self.assertEqual(parsed["thread_id"], "abc")
        self.assertFalse(parsed["completed"])
        self.assertIn("usage limit", parsed["error"])

        turn = AgentTurn(
            index=1, return_code=0, seconds=4.2, thread_id="abc",
            final_message="", usage=parsed["usage"],
            error=parsed["error"], completed=parsed["completed"],
        )
        self.assertFalse(turn.ok)
        self.assertTrue(turn.problems())

    def test_healthy_turn(self):
        stream = "\n".join([
            '{"type":"thread.started","thread_id":"abc"}',
            '{"type":"item.completed","item":{"type":"agent_message","text":"done"}}',
            '{"type":"turn.completed","usage":{"input_tokens":100,"output_tokens":50}}',
        ])
        parsed = _parse_codex_jsonl(stream)
        turn = AgentTurn(
            index=1, return_code=0, seconds=240.0, thread_id="abc",
            final_message=parsed["final_message"], usage=parsed["usage"],
            error=parsed["error"], completed=parsed["completed"],
        )
        self.assertTrue(turn.ok)
        self.assertEqual(turn.problems(), [])
        self.assertEqual(turn.usage.total, 150)
        self.assertEqual(turn.final_message, "done")

    def test_usage_accumulates(self):
        self.assertEqual((Usage(1, 2, 3) + Usage(4, 5, 6)).input_tokens, 5)


class NormalisationTests(unittest.TestCase):
    def test_subtracts_the_null_agent_floor(self):
        # 17/20 looks good, but 17 pass with no implementation at all.
        self.assertAlmostEqual(
            normalised_rate(17, 20, {"passed": 17, "total": 20}), 0.0
        )
        self.assertAlmostEqual(
            normalised_rate(20, 20, {"passed": 17, "total": 20}), 1.0
        )
        self.assertAlmostEqual(
            normalised_rate(6, 12, {"passed": 0, "total": 12}), 0.5
        )

    def test_no_signal_when_every_test_self_passes(self):
        self.assertIsNone(normalised_rate(26, 26, {"passed": 26, "total": 26}))

    def test_missing_calibration(self):
        self.assertIsNone(normalised_rate(10, 20, None))


class WorkspaceTests(unittest.TestCase):
    def test_workspace_hides_and_restores_tests(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            task = _demo_dataset(root)

            run = root / "results" / "r"
            with patch("migration_harness.core.subprocess.run"):
                ws = prepare_workspace(task, run)

            self.assertFalse((ws.agent_dir / "hidden.py").exists())
            self.assertTrue((ws.agent_dir / "_source_reference" / "A.java").exists())

            # Simulate agent tampering and implementation editing.
            (ws.agent_dir / "public.py").write_text("CHEAT = 1\n", encoding="utf-8")
            (ws.agent_dir / "run_tests.sh").write_text("exit 0 # cheated\n", encoding="utf-8")
            (ws.agent_dir / "impl.py").write_text("VALUE = 2\n", encoding="utf-8")

            pub = build_eval_workspace(task, ws, public_only=True)
            self.assertFalse((pub / "hidden.py").exists())
            self.assertEqual((pub / "public.py").read_text(encoding="utf-8"), "PUBLIC = 1\n")
            self.assertEqual((pub / "impl.py").read_text(encoding="utf-8"), "VALUE = 2\n")

            final = build_eval_workspace(task, ws, public_only=False)
            self.assertTrue((final / "hidden.py").exists())
            self.assertEqual((final / "public.py").read_text(encoding="utf-8"), "PUBLIC = 1\n")
            self.assertEqual((final / "run_tests.sh").read_text(encoding="utf-8"), "exit 0\n")

    @unittest.skipUnless(shutil.which("git"), "git required")
    def test_change_stats_distinguish_a_working_agent_from_a_dead_one(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            task = _demo_dataset(root)
            ws = prepare_workspace(task, root / "results" / "r")

            # An agent that crashed on startup changes nothing.
            self.assertEqual(agent_change_stats(ws.agent_dir)["files_changed"], 0)

            (ws.agent_dir / "new_module.py").write_text("x = 1\ny = 2\n", encoding="utf-8")
            stats = agent_change_stats(ws.agent_dir)
            self.assertEqual(stats["files_changed"], 1)
            self.assertEqual(stats["lines_added"], 2)

    @unittest.skipUnless(shutil.which("git"), "git required")
    def test_source_reference_excluded_from_diff(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            task = _demo_dataset(root)
            ws = prepare_workspace(task, root / "results" / "r")
            tracked = subprocess.run(
                ["git", "ls-files"], cwd=ws.agent_dir,
                capture_output=True, text=True,
            ).stdout
            self.assertNotIn("_source_reference", tracked)
            self.assertIn("impl.py", tracked)


class DatasetTests(unittest.TestCase):
    def test_dataset_root(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "data"
            (p / "source_projects").mkdir(parents=True)
            (p / "target_projects").mkdir()
            self.assertEqual(dataset_root(p), p.resolve())


if __name__ == "__main__":
    unittest.main()
