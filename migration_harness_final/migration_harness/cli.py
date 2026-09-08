from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import EXPERIMENTS, export_csv, iter_tasks, run_one, summary_text


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="migration-harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    ex = sub.add_parser("experiments")
    ex.set_defaults(handler=cmd_experiments)

    ls = sub.add_parser("list")
    ls.add_argument("--dataset", required=True)
    ls.add_argument("--source", default="Java")
    ls.add_argument("--target", default="Python")
    ls.add_argument("--limit", type=int, default=30)
    ls.set_defaults(handler=cmd_list)

    run = sub.add_parser("run")
    add_run_args(run)
    run.add_argument("--project", required=True)
    run.add_argument("--experiment", choices=list(EXPERIMENTS), default="baseline")
    run.add_argument("--replicate", type=int, default=1)
    run.set_defaults(handler=cmd_run)

    batch = sub.add_parser("batch")
    add_run_args(batch)
    batch.add_argument("--tasks", required=True, help="Text file: one project per line.")
    batch.add_argument("--experiment", choices=list(EXPERIMENTS), required=True)
    batch.add_argument("--replicates", type=int, default=1)
    batch.set_defaults(handler=cmd_batch)

    sm = sub.add_parser("summary")
    sm.add_argument("--results", default="results")
    sm.add_argument("--csv", default=None)
    sm.set_defaults(handler=cmd_summary)

    return p


def add_run_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--dataset", required=True)
    p.add_argument("--source", default="Java")
    p.add_argument("--target", default="Python")
    p.add_argument("--model", default=None)
    p.add_argument("--results", default="results")
    p.add_argument("--agent-timeout", type=int, default=1800)
    p.add_argument("--test-timeout", type=int, default=900)


def cmd_experiments(_: argparse.Namespace) -> int:
    for x in EXPERIMENTS.values():
        print(f"{x.name:10} {x.description}")
    return 0


def cmd_list(a: argparse.Namespace) -> int:
    tasks = [
        t for t in iter_tasks(a.dataset)
        if t.source == a.source and t.target == a.target
    ]
    print(f"{len(tasks)} tasks: {a.source} -> {a.target}")
    for t in tasks[:a.limit]:
        print(
            f"{t.project}\tpublic={len(t.public_tests)}"
            f"\thidden={len(t.hidden_tests)}"
        )
    return 0


def _run(a: argparse.Namespace, project: str, replicate: int) -> Path:
    return run_one(
        root=a.dataset,
        project=project,
        source=a.source,
        target=a.target,
        experiment_name=a.experiment,
        results_root=a.results,
        model=a.model,
        agent_timeout=a.agent_timeout,
        test_timeout=a.test_timeout,
        replicate=replicate,
    )


def cmd_run(a: argparse.Namespace) -> int:
    out = _run(a, a.project, a.replicate)
    print(out)
    return 0


def _read_tasks(path: str) -> list[str]:
    return [
        line.strip()
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def cmd_batch(a: argparse.Namespace) -> int:
    projects = _read_tasks(a.tasks)
    if not projects:
        raise ValueError("Tasks file is empty.")

    failures = 0
    for replicate in range(1, a.replicates + 1):
        for project in projects:
            print(
                f"== {a.experiment} | {project} | "
                f"replicate {replicate}/{a.replicates} =="
            )
            try:
                print(_run(a, project, replicate))
            except Exception as exc:
                failures += 1
                print(f"ERROR: {exc}", file=sys.stderr)

    return 1 if failures else 0


def cmd_summary(a: argparse.Namespace) -> int:
    print(summary_text(a.results))
    if a.csv:
        print(f"CSV: {export_csv(a.results, a.csv)}")
    return 0


def main() -> int:
    a = parser().parse_args()
    return a.handler(a)


if __name__ == "__main__":
    raise SystemExit(main())
