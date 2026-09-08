from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from migration_harness.core import (
    Task,
    build_eval_workspace,
    dataset_root,
    parse_test_output,
    prepare_workspace,
)


class CoreTests(unittest.TestCase):
    def test_pytest_parser(self):
        r = parse_test_output(
            "8 passed, 2 failed in 1.0s",
            "",
            1,
            1.0,
        )
        self.assertEqual(r.passed, 8)
        self.assertEqual(r.failed, 2)
        self.assertEqual(r.total, 10)
        self.assertAlmostEqual(r.pass_rate, 0.8)
        self.assertFalse(r.full_success)

    def test_unittest_parser(self):
        r = parse_test_output(
            "Ran 10 tests in 0.1s\nFAILED (failures=1, errors=2)",
            "",
            1,
            0.1,
        )
        self.assertEqual(r.passed, 7)
        self.assertEqual(r.failed, 3)

    def test_workspace_hides_and_restores_tests(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            src = root / "source_projects" / "Java" / "demo"
            tgt = root / "target_projects" / "Java" / "Python" / "demo"
            src.mkdir(parents=True)
            tgt.mkdir(parents=True)

            (src / "A.java").write_text("class A {}", encoding="utf-8")
            (tgt / "impl.py").write_text("VALUE = 1\n", encoding="utf-8")
            (tgt / "public.py").write_text("PUBLIC = 1\n", encoding="utf-8")
            (tgt / "hidden.py").write_text("HIDDEN = 1\n", encoding="utf-8")
            (tgt / "run_tests.sh").write_text("exit 0\n", encoding="utf-8")

            meta_dir = root / "target_projects"
            (meta_dir / "projects_summary.jsonl").write_text(
                json.dumps({
                    "project_name": "demo",
                    "source_language": "Java",
                    "target_language": "Python",
                    "target_public_tests": ["public.py"],
                    "target_original_tests": ["hidden.py"],
                    "run_tests_script": "run_tests.sh",
                }) + "\n",
                encoding="utf-8",
            )

            task = Task(root, {
                "project_name": "demo",
                "source_language": "Java",
                "target_language": "Python",
                "target_public_tests": ["public.py"],
                "target_original_tests": ["hidden.py"],
                "run_tests_script": "run_tests.sh",
            })

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
            self.assertEqual(
                (pub / "public.py").read_text(encoding="utf-8"),
                "PUBLIC = 1\n",
            )
            self.assertEqual(
                (pub / "impl.py").read_text(encoding="utf-8"),
                "VALUE = 2\n",
            )

            final = build_eval_workspace(task, ws, public_only=False)
            self.assertTrue((final / "hidden.py").exists())
            self.assertEqual(
                (final / "public.py").read_text(encoding="utf-8"),
                "PUBLIC = 1\n",
            )
            self.assertEqual(
                (final / "run_tests.sh").read_text(encoding="utf-8"),
                "exit 0\n",
            )

    def test_dataset_root(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "data"
            (p / "source_projects").mkdir(parents=True)
            (p / "target_projects").mkdir()
            self.assertEqual(dataset_root(p), p.resolve())


if __name__ == "__main__":
    unittest.main()
