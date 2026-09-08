from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# Experiment definitions
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Experiment:
    name: str
    planning: bool
    feedback_rounds: int
    completion_gate: bool
    description: str


EXPERIMENTS: dict[str, Experiment] = {
    "baseline": Experiment(
        name="baseline",
        planning=False,
        feedback_rounds=0,
        completion_gate=False,
        description="Single off-the-shelf Codex migration pass.",
    ),
    "planning": Experiment(
        name="planning",
        planning=True,
        feedback_rounds=0,
        completion_gate=False,
        description="Baseline plus mandatory repository analysis and planning.",
    ),
    "feedback": Experiment(
        name="feedback",
        planning=True,
        feedback_rounds=1,
        completion_gate=False,
        description="Planning plus one deterministic public-test repair round.",
    ),
    "gate": Experiment(
        name="gate",
        planning=True,
        feedback_rounds=3,
        completion_gate=True,
        description="Planning plus public-test completion gate (up to 3 repairs).",
    ),
}


# ---------------------------------------------------------------------------
# RepoTransBench model / discovery
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Task:
    dataset_root: Path
    metadata: dict[str, Any]

    @property
    def project(self) -> str:
        return str(self.metadata["project_name"])

    @property
    def source(self) -> str:
        return str(self.metadata["source_language"])

    @property
    def target(self) -> str:
        return str(self.metadata["target_language"])

    @property
    def source_dir(self) -> Path:
        return self.dataset_root / "source_projects" / self.source / self.project

    @property
    def target_dir(self) -> Path:
        # RepoTransBench's own agent uses source/target ordering.
        return (
            self.dataset_root
            / "target_projects"
            / self.source
            / self.target
            / self.project
        )

    @property
    def public_tests(self) -> list[str]:
        return [str(x) for x in self.metadata.get("target_public_tests", []) or []]

    @property
    def hidden_tests(self) -> list[str]:
        # RepoTransBench calls these target_original_tests.
        return [str(x) for x in self.metadata.get("target_original_tests", []) or []]

    @property
    def test_script(self) -> str:
        return str(self.metadata.get("run_tests_script", "run_tests.sh"))


def dataset_root(path: str | Path) -> Path:
    """
    Accept either the actual dataset root or a parent directory containing it.
    The root must directly contain source_projects/ and target_projects/.
    """
    p = Path(path).expanduser().resolve()
    if (
        (p / "source_projects").is_dir()
        and (p / "target_projects").is_dir()
    ):
        return p

    if p.is_dir():
        for target_projects in p.rglob("target_projects"):
            candidate = target_projects.parent
            if (
                (candidate / "source_projects").is_dir()
                and (candidate / "target_projects").is_dir()
            ):
                return candidate

    raise FileNotFoundError(
        f"Could not find RepoTransBench dataset under {p}. "
        "Expected source_projects/ and target_projects/."
    )


def iter_tasks(root: str | Path) -> Iterable[Task]:
    root = dataset_root(root)
    summary = root / "target_projects" / "projects_summary.jsonl"
    if not summary.exists():
        raise FileNotFoundError(f"Missing {summary}")

    with summary.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield Task(root, json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {summary} line {line_no}"
                ) from exc


def find_task(
    root: str | Path,
    project: str,
    source: str,
    target: str,
) -> Task:
    matches = [
        t for t in iter_tasks(root)
        if t.project == project and t.source == source and t.target == target
    ]
    if not matches:
        raise LookupError(f"No task: {source} -> {target}, {project!r}")
    if len(matches) > 1:
        raise LookupError(f"Ambiguous task: {source} -> {target}, {project!r}")

    task = matches[0]
    if not task.source_dir.is_dir():
        raise FileNotFoundError(f"Missing source project: {task.source_dir}")
    if not task.target_dir.is_dir():
        raise FileNotFoundError(f"Missing target project: {task.target_dir}")
    return task


# ---------------------------------------------------------------------------
# Workspace isolation
# ---------------------------------------------------------------------------

SOURCE_REFERENCE = "_source_reference"


@dataclass(frozen=True)
class Workspace:
    run_dir: Path
    agent_dir: Path
    public_eval_dir: Path
    final_eval_dir: Path


def _norm(rel: str) -> str:
    return Path(rel).as_posix().lstrip("./")


def _remove(root: Path, rel: str) -> None:
    p = root / rel
    if p.is_dir():
        shutil.rmtree(p)
    elif p.exists():
        p.unlink()


def _copy_path(src_root: Path, dst_root: Path, rel: str) -> None:
    src = src_root / rel
    dst = dst_root / rel

    if dst.is_dir():
        shutil.rmtree(dst)
    elif dst.exists():
        dst.unlink()

    if not src.exists():
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def prepare_workspace(task: Task, run_dir: Path) -> Workspace:
    """
    Agent sees:
      - target repository scaffold
      - public tests
      - pristine test runner
      - complete source repository at _source_reference/
    Agent does NOT see target_original_tests.
    """
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)

    agent = run_dir / "agent"
    public_eval = run_dir / "public_eval"
    final_eval = run_dir / "final_eval"

    shutil.copytree(task.target_dir, agent)

    for rel in task.hidden_tests:
        _remove(agent, rel)

    shutil.copytree(task.source_dir, agent / SOURCE_REFERENCE)

    # A Git worktree makes Codex's repository behavior predictable.
    subprocess.run(
        ["git", "init", "-q"],
        cwd=agent,
        check=True,
        capture_output=True,
        text=True,
    )

    return Workspace(run_dir, agent, public_eval, final_eval)


def _copy_agent_tree(agent: Path, dst: Path) -> None:
    """
    Copy the exact agent-produced tree, excluding harness-only directories.
    Starting from the agent tree (rather than pristine target) preserves agent
    deletions of implementation files.
    """
    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = set()
        path = Path(directory)
        if path == agent:
            ignored.update({".git", SOURCE_REFERENCE})
        return ignored

    shutil.copytree(agent, dst, ignore=ignore)


def build_eval_workspace(
    task: Task,
    ws: Workspace,
    *,
    public_only: bool,
) -> Path:
    """
    Rebuild evaluation from agent output, then restore benchmark-owned files.

    This ensures edits to tests or run_tests.sh can never improve the score.
    """
    dst = ws.public_eval_dir if public_only else ws.final_eval_dir
    if dst.exists():
        shutil.rmtree(dst)

    _copy_agent_tree(ws.agent_dir, dst)

    # Restore pristine public tests and test runner.
    _copy_path(task.target_dir, dst, task.test_script)
    for rel in task.public_tests:
        _copy_path(task.target_dir, dst, rel)

    if public_only:
        # Held-out tests must not participate in agent feedback.
        for rel in task.hidden_tests:
            _remove(dst, rel)
    else:
        # Restore pristine held-out tests only for final evaluation.
        for rel in task.hidden_tests:
            _copy_path(task.target_dir, dst, rel)

    return dst


# ---------------------------------------------------------------------------
# Codex CLI adapter
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Usage:
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0

    def __add__(self, other: "Usage") -> "Usage":
        return Usage(
            self.input_tokens + other.input_tokens,
            self.cached_input_tokens + other.cached_input_tokens,
            self.output_tokens + other.output_tokens,
        )


@dataclass(frozen=True)
class AgentTurn:
    index: int
    return_code: int
    seconds: float
    thread_id: str | None
    final_message: str
    usage: Usage


def require_codex() -> None:
    if not shutil.which("codex"):
        raise RuntimeError(
            "`codex` is not on PATH. Install/authenticate Codex CLI first."
        )


def _parse_codex_jsonl(text: str) -> tuple[str | None, str, Usage]:
    thread_id = None
    final_message = ""
    usage = Usage()

    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue

        if event.get("type") == "thread.started":
            thread_id = event.get("thread_id") or thread_id

        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                final_message = str(item.get("text", ""))

        if event.get("type") == "turn.completed":
            u = event.get("usage") or {}
            usage = Usage(
                input_tokens=int(u.get("input_tokens", 0) or 0),
                cached_input_tokens=int(u.get("cached_input_tokens", 0) or 0),
                output_tokens=int(u.get("output_tokens", 0) or 0),
            )

    return thread_id, final_message, usage


def run_codex(
    workspace: Path,
    prompt: str,
    *,
    turn_index: int,
    log_dir: Path,
    timeout: int,
    model: str | None = None,
    thread_id: str | None = None,
) -> AgentTurn:
    """
    Non-interactive Codex invocation.

    Current CLI shape:
      codex -a never exec --sandbox workspace-write --json ...
      codex -a never exec --sandbox workspace-write --json resume THREAD ...
    """
    require_codex()
    log_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "codex",
        "-a", "never",
        "exec",
        "--sandbox", "workspace-write",
        "--json",
    ]
    if model:
        cmd += ["--model", model]
    if thread_id:
        cmd += ["resume", thread_id]
    cmd += [prompt]

    started = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            stdin=subprocess.DEVNULL,
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        stderr += "\nHARNESS_AGENT_TIMEOUT\n"
        code = 124

    seconds = time.monotonic() - started

    (log_dir / f"turn_{turn_index:02d}.jsonl").write_text(
        stdout, encoding="utf-8"
    )
    (log_dir / f"turn_{turn_index:02d}.stderr.txt").write_text(
        stderr, encoding="utf-8"
    )

    parsed_thread, final_message, usage = _parse_codex_jsonl(stdout)
    return AgentTurn(
        index=turn_index,
        return_code=code,
        seconds=seconds,
        thread_id=parsed_thread or thread_id,
        final_message=final_message,
        usage=usage,
    )


# ---------------------------------------------------------------------------
# Test execution / metrics
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TestResult:
    return_code: int
    seconds: float
    passed: int | None
    failed: int | None
    total: int | None
    pass_rate: float | None
    full_success: bool
    parser: str


def _last(pattern: str, text: str) -> int:
    hits = re.findall(pattern, text, flags=re.IGNORECASE)
    return int(hits[-1]) if hits else 0


def parse_test_output(
    stdout: str,
    stderr: str,
    return_code: int,
    seconds: float,
) -> TestResult:
    text = stdout + "\n" + stderr

    # Pytest-style summary.
    passed = _last(r"(\d+)\s+passed\b", text)
    failed = _last(r"(\d+)\s+failed\b", text)
    errors = _last(r"(\d+)\s+errors?\b", text)
    skipped = _last(r"(\d+)\s+skipped\b", text)

    if any((passed, failed, errors, skipped)):
        failing = failed + errors
        total = passed + failing
        return TestResult(
            return_code, seconds, passed, failing, total or None,
            (passed / total) if total else None,
            return_code == 0, "pytest",
        )

    # unittest-style summary.
    ran = re.findall(r"Ran\s+(\d+)\s+tests?", text, flags=re.IGNORECASE)
    if ran:
        total = int(ran[-1])
        failures = _last(r"failures=(\d+)", text)
        errors = _last(r"errors=(\d+)", text)
        failing = failures + errors
        passed = max(total - failing, 0)
        return TestResult(
            return_code, seconds, passed, failing, total,
            passed / total if total else None,
            return_code == 0, "unittest",
        )

    # The benchmark's process status is always authoritative for full success.
    return TestResult(
        return_code, seconds, None, None, None, None,
        return_code == 0, "exit_code",
    )


def run_tests(
    task: Task,
    workspace: Path,
    *,
    timeout: int,
    log_prefix: Path,
) -> tuple[TestResult, str, str]:
    script = workspace / task.test_script
    if not script.exists():
        raise FileNotFoundError(f"Missing benchmark test script: {script}")

    started = time.monotonic()
    try:
        proc = subprocess.run(
            ["bash", str(script)],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        stderr += "\nHARNESS_TEST_TIMEOUT\n"
        code = 124

    seconds = time.monotonic() - started
    result = parse_test_output(stdout, stderr, code, seconds)

    log_prefix.parent.mkdir(parents=True, exist_ok=True)
    log_prefix.with_suffix(".stdout.txt").write_text(stdout, encoding="utf-8")
    log_prefix.with_suffix(".stderr.txt").write_text(stderr, encoding="utf-8")
    log_prefix.with_suffix(".json").write_text(
        json.dumps(asdict(result), indent=2),
        encoding="utf-8",
    )
    return result, stdout, stderr


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def initial_prompt(task: Task, experiment: Experiment) -> str:
    prompt = f"""\
Migrate this repository from {task.source} to {task.target}.

The complete original {task.source} repository is under `{SOURCE_REFERENCE}/`.
The current working directory is the target repository.

Requirements:
- Preserve the source repository's externally observable behavior.
- Implement the target repository completely; do not use stubs or hard-coded
  answers for visible tests.
- You may inspect the visible public tests and the benchmark test runner.
- Do not modify tests, the benchmark test runner, or `{SOURCE_REFERENCE}/`.
- Work only inside this repository.
"""
    if experiment.planning:
        prompt += """\

Before editing:
1. Inspect the full source tree and target scaffold.
2. Identify the public API, dependencies, resources/configuration, and tests.
3. Form a concise migration plan mapping source components to target components.
4. Then implement the plan completely.
"""
    prompt += "\nWhen you believe the migration is complete, stop.\n"
    return prompt


def repair_prompt(
    result: TestResult,
    stdout: str,
    stderr: str,
    *,
    round_no: int,
    completion_gate: bool,
) -> str:
    output = (stdout + "\n" + stderr).strip()
    max_chars = 16000
    if len(output) > max_chars:
        output = "[earlier output truncated]\n" + output[-max_chars:]

    gate = (
        "The harness will not accept completion while these deterministic "
        "public checks fail. "
        if completion_gate else ""
    )
    return f"""\
Public-test feedback round {round_no}.

{gate}The pristine public-test run failed with exit code {result.return_code}.
Fix the implementation. Do not edit tests or the benchmark test runner.

----- TEST OUTPUT -----
{output}
----- END TEST OUTPUT -----
"""


# ---------------------------------------------------------------------------
# One complete experiment run
# ---------------------------------------------------------------------------

def run_one(
    *,
    root: str | Path,
    project: str,
    source: str,
    target: str,
    experiment_name: str,
    results_root: str | Path = "results",
    model: str | None = None,
    agent_timeout: int = 1800,
    test_timeout: int = 900,
    replicate: int = 1,
) -> Path:
    if experiment_name not in EXPERIMENTS:
        raise ValueError(
            f"Unknown experiment {experiment_name!r}; "
            f"choose {', '.join(EXPERIMENTS)}"
        )

    experiment = EXPERIMENTS[experiment_name]
    task = find_task(root, project, source, target)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_project = re.sub(r"[^A-Za-z0-9_.-]+", "_", project)
    run_dir = (
        Path(results_root)
        / experiment.name
        / f"{stamp}_{source}_to_{target}_{safe_project}_r{replicate}"
    )

    ws = prepare_workspace(task, run_dir)
    logs = run_dir / "agent_logs"

    prompt = initial_prompt(task, experiment)
    (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    turns: list[AgentTurn] = []
    public_results: list[TestResult] = []

    first = run_codex(
        ws.agent_dir,
        prompt,
        turn_index=1,
        log_dir=logs,
        timeout=agent_timeout,
        model=model,
    )
    turns.append(first)

    thread_id = first.thread_id
    if experiment.feedback_rounds and not thread_id:
        raise RuntimeError(
            "Codex JSON output did not provide a thread id; "
            "cannot perform repair turns."
        )

    for round_no in range(1, experiment.feedback_rounds + 1):
        public_ws = build_eval_workspace(task, ws, public_only=True)
        test_result, stdout, stderr = run_tests(
            task,
            public_ws,
            timeout=test_timeout,
            log_prefix=run_dir / f"public_round_{round_no:02d}",
        )
        public_results.append(test_result)

        if test_result.full_success:
            break

        follow_up = repair_prompt(
            test_result,
            stdout,
            stderr,
            round_no=round_no,
            completion_gate=experiment.completion_gate,
        )
        (run_dir / f"repair_prompt_{round_no:02d}.txt").write_text(
            follow_up, encoding="utf-8"
        )

        turn = run_codex(
            ws.agent_dir,
            follow_up,
            turn_index=len(turns) + 1,
            log_dir=logs,
            timeout=agent_timeout,
            model=model,
            thread_id=thread_id,
        )
        turns.append(turn)

        if turn.thread_id and turn.thread_id != thread_id:
            raise RuntimeError(
                "Codex resumed into a different thread; refusing invalid run."
            )

    # Held-out/original tests are restored only here and never fed back.
    final_ws = build_eval_workspace(task, ws, public_only=False)
    final_result, _, _ = run_tests(
        task,
        final_ws,
        timeout=test_timeout,
        log_prefix=run_dir / "final",
    )

    usage = Usage()
    for turn in turns:
        usage = usage + turn.usage

    payload = {
        "schema_version": 1,
        "timestamp_utc": stamp,
        "experiment": asdict(experiment),
        "task": {
            "project": task.project,
            "source": task.source,
            "target": task.target,
            "public_test_paths": len(task.public_tests),
            "hidden_test_paths": len(task.hidden_tests),
        },
        "replicate": replicate,
        "model": model,
        "agent": {
            "turns": [asdict(x) for x in turns],
            "turn_count": len(turns),
            "seconds": sum(x.seconds for x in turns),
            "usage": asdict(usage),
        },
        "public_checks": [asdict(x) for x in public_results],
        "final": asdict(final_result),
    }

    out = run_dir / "result.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def load_results(results_root: str | Path) -> list[dict[str, Any]]:
    return [
        json.loads(p.read_text(encoding="utf-8"))
        for p in Path(results_root).glob("*/*/result.json")
    ]


def summary_text(results_root: str | Path) -> str:
    rows = load_results(results_root)
    if not rows:
        return "No results found."

    by_exp: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_exp.setdefault(row["experiment"]["name"], []).append(row)

    lines = []
    for name in EXPERIMENTS:
        group = by_exp.get(name, [])
        if not group:
            continue

        successes = [bool(x["final"]["full_success"]) for x in group]
        rates = [
            x["final"]["pass_rate"]
            for x in group
            if x["final"]["pass_rate"] is not None
        ]
        turns = [x["agent"]["turn_count"] for x in group]
        seconds = [x["agent"]["seconds"] for x in group]

        lines.append(f"{name}:")
        lines.append(
            f"  success: {sum(successes)}/{len(group)} "
            f"({sum(successes)/len(group):.1%})"
        )
        lines.append(
            f"  mean test pass rate: "
            f"{mean(rates):.1%}" if rates else
            "  mean test pass rate: n/a"
        )
        lines.append(f"  mean agent turns: {mean(turns):.2f}")
        lines.append(f"  mean agent time: {mean(seconds):.1f}s")

    return "\n".join(lines)


def export_csv(results_root: str | Path, output: str | Path) -> Path:
    rows = load_results(results_root)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "experiment", "project", "replicate", "full_success",
        "pass_rate", "passed", "failed", "total",
        "agent_turns", "agent_seconds",
        "input_tokens", "cached_input_tokens", "output_tokens",
    ]
    with output.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for x in rows:
            final = x["final"]
            usage = x["agent"]["usage"]
            w.writerow({
                "experiment": x["experiment"]["name"],
                "project": x["task"]["project"],
                "replicate": x["replicate"],
                "full_success": final["full_success"],
                "pass_rate": final["pass_rate"],
                "passed": final["passed"],
                "failed": final["failed"],
                "total": final["total"],
                "agent_turns": x["agent"]["turn_count"],
                "agent_seconds": x["agent"]["seconds"],
                "input_tokens": usage["input_tokens"],
                "cached_input_tokens": usage["cached_input_tokens"],
                "output_tokens": usage["output_tokens"],
            })
    return output
