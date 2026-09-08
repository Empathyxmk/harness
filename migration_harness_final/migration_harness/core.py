from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Iterable


SCHEMA_VERSION = 2


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
    def all_tests(self) -> list[str]:
        return self.public_tests + self.hidden_tests

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
# Reproducibility metadata
# ---------------------------------------------------------------------------

def _cmd_output(cmd: list[str], cwd: Path | None = None) -> str | None:
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=30
        )
    except Exception:  # noqa: BLE001
        return None
    out = (proc.stdout or "").strip()
    return out.splitlines()[0] if out else None


def codex_config_fingerprint() -> dict[str, Any]:
    """
    Codex reads ~/.codex/config.toml, which lives outside the repository and
    silently changes reasoning effort, sandbox policy and model defaults.
    Record enough to detect drift between runs.
    """
    path = Path.home() / ".codex" / "config.toml"
    if not path.exists():
        return {"path": str(path), "present": False}

    text = path.read_text(encoding="utf-8", errors="replace")
    interesting: dict[str, str] = {}
    for key in (
        "model", "model_reasoning_effort", "model_reasoning_summary",
        "approval_policy", "sandbox_mode",
    ):
        m = re.search(rf'^\s*{key}\s*=\s*"?([^"\n#]+)"?', text, flags=re.MULTILINE)
        if m:
            interesting[key] = m.group(1).strip()

    return {
        "path": str(path),
        "present": True,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
        "settings": interesting,
    }


def environment_metadata(harness_root: Path | None = None) -> dict[str, Any]:
    root = harness_root or Path(__file__).resolve().parent.parent
    return {
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "harness_commit": _cmd_output(["git", "rev-parse", "HEAD"], cwd=root),
        "harness_dirty": bool(
            _cmd_output(["git", "status", "--porcelain"], cwd=root)
        ),
        "codex_version": _cmd_output(["codex", "--version"]),
        "codex_config": codex_config_fingerprint(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "pytest_version": _cmd_output(
            [sys.executable, "-m", "pytest", "--version"]
        ),
    }


# ---------------------------------------------------------------------------
# Workspace isolation
# ---------------------------------------------------------------------------

SOURCE_REFERENCE = "_source_reference"
BASELINE_COMMIT_MESSAGE = "harness: pristine target scaffold"


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


def _git(agent: Path, *args: str, check: bool = True) -> None:
    subprocess.run(
        [
            "git",
            "-c", "user.name=migration-harness",
            "-c", "user.email=harness@localhost",
            "-c", "commit.gpgsign=false",
            *args,
        ],
        cwd=agent,
        check=check,
        capture_output=True,
        text=True,
    )


def prepare_workspace(task: Task, run_dir: Path) -> Workspace:
    """
    Agent sees:
      - target repository scaffold
      - public tests
      - pristine test runner
      - complete source repository at _source_reference/
    Agent does NOT see target_original_tests.

    The scaffold is committed so that everything the agent writes is visible
    as a diff against HEAD afterwards. Without this there is no way to tell a
    completed migration from an agent that never ran.
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
    _git(agent, "init", "-q")

    # Keep the source reference out of the diff without hiding it from the agent.
    exclude = agent / ".git" / "info" / "exclude"
    if exclude.parent.is_dir():
        exclude.write_text(f"{SOURCE_REFERENCE}/\n", encoding="utf-8")

    _git(agent, "add", "-A")
    _git(agent, "commit", "-q", "--allow-empty", "-m", BASELINE_COMMIT_MESSAGE)

    return Workspace(run_dir, agent, public_eval, final_eval)


def agent_change_stats(agent: Path) -> dict[str, Any]:
    """
    Files and lines the agent wrote, measured against the committed scaffold.
    Returns zeros (not an error) when git is unavailable, so this can never
    break a run.
    """
    empty = {"files_changed": None, "lines_added": None, "lines_removed": None}
    try:
        _git(agent, "add", "-A", check=False)
        proc = subprocess.run(
            ["git", "diff", "--cached", "--numstat", "HEAD"],
            cwd=agent, capture_output=True, text=True, timeout=120,
        )
        if proc.returncode != 0:
            return empty

        files = added = removed = 0
        for line in (proc.stdout or "").splitlines():
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            files += 1
            if parts[0].isdigit():
                added += int(parts[0])
            if parts[1].isdigit():
                removed += int(parts[1])
        return {
            "files_changed": files,
            "lines_added": added,
            "lines_removed": removed,
        }
    except Exception:  # noqa: BLE001
        return empty


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

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass(frozen=True)
class AgentTurn:
    index: int
    return_code: int
    seconds: float
    thread_id: str | None
    final_message: str
    usage: Usage
    error: str | None = None
    completed: bool = True

    @property
    def ok(self) -> bool:
        return (
            self.return_code == 0
            and self.error is None
            and self.completed
            and self.usage.total > 0
        )

    def problems(self) -> list[str]:
        out = []
        if self.error:
            out.append(f"agent error: {self.error}")
        if self.return_code != 0:
            out.append(f"non-zero exit {self.return_code}")
        if not self.completed:
            out.append("no turn.completed event")
        if self.usage.total == 0:
            out.append("zero token usage")
        return out


class AgentUnavailable(RuntimeError):
    """The agent could not run at all (quota, auth, bad model, crash)."""


def require_codex() -> None:
    if not shutil.which("codex"):
        raise RuntimeError(
            "`codex` is not on PATH. Install/authenticate Codex CLI first."
        )


def _parse_codex_jsonl(text: str) -> dict[str, Any]:
    """
    Codex reports failures inside the JSON event stream (`error` /
    `turn.failed`) while the process itself may still exit zero, so the exit
    code alone is not a reliable health signal.
    """
    thread_id: str | None = None
    final_message = ""
    usage = Usage()
    error: str | None = None
    completed = False

    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue

        etype = event.get("type")

        if etype == "thread.started":
            thread_id = event.get("thread_id") or thread_id

        elif etype == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                final_message = str(item.get("text", ""))

        elif etype == "turn.completed":
            completed = True
            u = event.get("usage") or {}
            usage = usage + Usage(
                input_tokens=int(u.get("input_tokens", 0) or 0),
                cached_input_tokens=int(u.get("cached_input_tokens", 0) or 0),
                output_tokens=int(u.get("output_tokens", 0) or 0),
            )

        elif etype in ("error", "turn.failed"):
            msg = event.get("message")
            if not msg:
                msg = (event.get("error") or {}).get("message")
            if msg and not error:
                error = str(msg)

    return {
        "thread_id": thread_id,
        "final_message": final_message,
        "usage": usage,
        "error": error,
        "completed": completed,
    }


def run_codex(
    workspace: Path,
    prompt: str,
    *,
    turn_index: int,
    log_dir: Path,
    timeout: int,
    model: str | None = None,
    thread_id: str | None = None,
    sandbox: str = "workspace-write",
) -> AgentTurn:
    """
    Non-interactive Codex invocation.

    Current CLI shape:
      codex -a never exec --sandbox workspace-write --skip-git-repo-check --json ...
      codex -a never exec --sandbox workspace-write --skip-git-repo-check --json resume THREAD ...

    --skip-git-repo-check keeps the run independent of Codex's per-directory
    trust state, which is machine-local and would otherwise silently decide
    whether a run happens.
    """
    require_codex()
    log_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "codex",
        "-a", "never",
        "exec",
        "--sandbox", sandbox,
        "--skip-git-repo-check",
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

    parsed = _parse_codex_jsonl(stdout)
    error = parsed["error"]
    if error is None and code == 124:
        error = "agent timeout"
    if error is None and code != 0 and not parsed["completed"]:
        error = (stderr.strip() or "codex exited non-zero")[-300:]

    return AgentTurn(
        index=turn_index,
        return_code=code,
        seconds=seconds,
        thread_id=parsed["thread_id"] or thread_id,
        final_message=parsed["final_message"],
        usage=parsed["usage"],
        error=error,
        completed=parsed["completed"],
    )


def probe_agent(model: str | None = None, timeout: int = 180) -> tuple[bool, str]:
    """
    One cheap agent call under the same conditions a real run uses. Call this
    before a batch so that quota exhaustion costs seconds instead of a whole
    experiment's worth of empty runs.
    """
    require_codex()
    import tempfile

    d = Path(tempfile.mkdtemp(prefix="harness_probe_"))
    try:
        _git(d, "init", "-q", check=False)
        turn = run_codex(
            d,
            "Reply with exactly: PROBE_OK",
            turn_index=0,
            log_dir=d / "logs",
            timeout=timeout,
            model=model,
        )
        if turn.ok:
            return True, "ok"
        return False, "; ".join(turn.problems())
    finally:
        shutil.rmtree(d, ignore_errors=True)


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
    count_source: str = "run_tests_script"
    # The benchmark script's own verdict, kept separately from full_success so
    # the stricter harness verdict stays auditable against RepoTransBench's.
    script_success: bool | None = None
    fixed_list_success: bool | None = None


def _sum(pattern: str, text: str) -> int:
    """
    Sum every occurrence rather than taking the last one.

    Several RepoTransBench run_tests.sh scripts invoke pytest more than once
    ("pytest tests/" then "pytest public_tests/"). Reading only the final
    summary block discards the first invocation, and because those scripts use
    `set -e`, a failure in the first invocation prevents the second from
    running at all -- which shrinks the denominator exactly when the agent does
    badly, making pass rates incomparable between runs.
    """
    return sum(int(x) for x in re.findall(pattern, text, flags=re.IGNORECASE))


def parse_test_output(
    stdout: str,
    stderr: str,
    return_code: int,
    seconds: float,
) -> TestResult:
    text = stdout + "\n" + stderr

    # Pytest-style summary.
    passed = _sum(r"(\d+)\s+passed\b", text)
    failed = _sum(r"(\d+)\s+failed\b", text)
    errors = _sum(r"(\d+)\s+errors?\b", text)
    skipped = _sum(r"(\d+)\s+skipped\b", text)

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
        total = sum(int(x) for x in ran)
        failures = _sum(r"failures=(\d+)", text)
        errors = _sum(r"errors=(\d+)", text)
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
    """Run the benchmark's own script. Its exit code defines full success."""
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


def count_tests(
    workspace: Path,
    test_paths: list[str],
    *,
    timeout: int,
    log_prefix: Path,
) -> TestResult | None:
    """
    Count passes and failures with a single pytest invocation over an explicit,
    fixed list of test files.

    This exists because the denominator produced by run_tests.sh is not stable:
    scripts that call pytest twice under `set -e` stop after the first failure,
    so a worse agent can post a *higher* pass rate simply because fewer tests
    ran. Comparing variants requires the same denominator every time.

    Runs after run_tests.sh so that any dependency installation the script
    performs has already happened. Returns None if nothing usable was parsed,
    in which case the caller falls back to the script's own numbers.
    """
    present = [p for p in test_paths if (workspace / p).exists()]
    if not present:
        return None

    started = time.monotonic()
    try:
        proc = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "--tb=no", "-q", "-p", "no:cacheprovider",
                *present,
            ],
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=timeout,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        stdout, stderr, code = proc.stdout or "", proc.stderr or "", proc.returncode
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        stderr += "\nHARNESS_COUNT_TIMEOUT\n"
        code = 124
    except Exception:  # noqa: BLE001
        return None

    seconds = time.monotonic() - started
    parsed = parse_test_output(stdout, stderr, code, seconds)
    if parsed.total is None:
        return None

    log_prefix.parent.mkdir(parents=True, exist_ok=True)
    log_prefix.with_suffix(".stdout.txt").write_text(stdout, encoding="utf-8")
    log_prefix.with_suffix(".stderr.txt").write_text(stderr, encoding="utf-8")
    return parsed


def evaluate(
    task: Task,
    workspace: Path,
    *,
    timeout: int,
    log_prefix: Path,
    test_paths: list[str],
) -> tuple[TestResult, str, str]:
    """
    Authoritative evaluation.

    passed/total   <- one pytest invocation over a fixed file list
    script_success <- the benchmark's own run_tests.sh exit code
    full_success   <- BOTH must succeed

    Requiring both closes a loophole in the benchmark's own runners: several
    run_tests.sh scripts execute only a subset of the declared test files (for
    example `pytest tests/` with `set -e`, so public_tests/ never runs after a
    failure), and would therefore report success while declared benchmark tests
    fail. script_success is kept in the record so the two verdicts can always be
    compared.
    """
    script_result, stdout, stderr = run_tests(
        task, workspace, timeout=timeout, log_prefix=log_prefix
    )

    counted = count_tests(
        workspace,
        test_paths,
        timeout=timeout,
        log_prefix=log_prefix.with_name(log_prefix.name + "_count"),
    )

    if counted is None:
        # No countable fixed-list run; the script's verdict is all there is.
        fallback = TestResult(
            return_code=script_result.return_code,
            seconds=script_result.seconds,
            passed=script_result.passed,
            failed=script_result.failed,
            total=script_result.total,
            pass_rate=script_result.pass_rate,
            full_success=script_result.full_success,
            parser=script_result.parser,
            count_source=script_result.count_source,
            script_success=script_result.full_success,
            fixed_list_success=None,
        )
        log_prefix.with_suffix(".json").write_text(
            json.dumps(asdict(fallback), indent=2), encoding="utf-8"
        )
        return fallback, stdout, stderr

    fixed_list_success = counted.return_code == 0

    merged = TestResult(
        return_code=script_result.return_code,
        seconds=script_result.seconds,
        passed=counted.passed,
        failed=counted.failed,
        total=counted.total,
        pass_rate=counted.pass_rate,
        full_success=script_result.full_success and fixed_list_success,
        parser=counted.parser,
        count_source="fixed_test_list",
        script_success=script_result.full_success,
        fixed_list_success=fixed_list_success,
    )
    log_prefix.with_suffix(".json").write_text(
        json.dumps(asdict(merged), indent=2), encoding="utf-8"
    )
    return merged, stdout, stderr


# ---------------------------------------------------------------------------
# Null-agent calibration
# ---------------------------------------------------------------------------

def null_baseline(
    task: Task,
    *,
    work_root: Path,
    test_timeout: int = 900,
) -> dict[str, Any]:
    """
    Score the untouched scaffold: what the harness reports when the agent
    writes nothing at all.

    Many RepoTransBench test files are self-contained -- they define the
    classes under test inside the test file -- so they pass against an empty
    repository. Without this figure, a raw pass rate cannot be interpreted and
    differences between experiment variants cannot be attributed to the agent.
    """
    run_dir = work_root / f"null_{re.sub(r'[^A-Za-z0-9_.-]+', '_', task.project)}"
    ws = prepare_workspace(task, run_dir)
    final_ws = build_eval_workspace(task, ws, public_only=False)
    result, _, _ = evaluate(
        task,
        final_ws,
        timeout=test_timeout,
        log_prefix=run_dir / "null_final",
        test_paths=task.all_tests,
    )
    return {
        "project": task.project,
        "source": task.source,
        "target": task.target,
        "passed": result.passed,
        "total": result.total,
        "pass_rate": result.pass_rate,
        "full_success": result.full_success,
        "count_source": result.count_source,
    }


def calibrate(
    root: str | Path,
    projects: list[str],
    *,
    source: str,
    target: str,
    results_root: str | Path,
    test_timeout: int = 900,
    progress=print,
) -> Path:
    import tempfile

    results = Path(results_root)
    results.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="harness_calibrate_"))

    out: dict[str, Any] = {}
    try:
        for i, name in enumerate(projects, 1):
            task = find_task(root, name, source, target)
            row = null_baseline(task, work_root=work, test_timeout=test_timeout)
            out[name] = row
            rate = "n/a" if row["pass_rate"] is None else f"{row['pass_rate']:.1%}"
            progress(
                f"[{i}/{len(projects)}] {name}: "
                f"null agent {row['passed']}/{row['total']} ({rate})"
            )
    finally:
        shutil.rmtree(work, ignore_errors=True)

    path = results / "null_baseline.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return path


def load_null_baseline(results_root: str | Path) -> dict[str, Any]:
    path = Path(results_root) / "null_baseline.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def normalised_rate(
    passed: int | None,
    total: int | None,
    null_row: dict[str, Any] | None,
) -> float | None:
    """
    Share of the tests that actually depend on the agent's work.

        (passed - null_passed) / (total - null_passed)

    Returns None when every test already passes without an implementation, in
    which case the task carries no signal at all.
    """
    if not null_row or passed is None or not total:
        return None
    np_ = null_row.get("passed")
    if np_ is None:
        return None
    denominator = total - np_
    if denominator <= 0:
        return None
    return (passed - np_) / denominator


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
    strict: bool = True,
) -> Path:
    """
    strict=True (default) raises AgentUnavailable as soon as the agent fails to
    do any work, so a batch stops instead of filling the results directory with
    runs that only measure the benchmark's self-passing tests.
    """
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

    agent_problems = list(first.problems())

    thread_id = first.thread_id
    if not agent_problems and experiment.feedback_rounds and not thread_id:
        raise RuntimeError(
            "Codex JSON output did not provide a thread id; "
            "cannot perform repair turns."
        )

    if not agent_problems:
        for round_no in range(1, experiment.feedback_rounds + 1):
            public_ws = build_eval_workspace(task, ws, public_only=True)
            test_result, stdout, stderr = evaluate(
                task,
                public_ws,
                timeout=test_timeout,
                log_prefix=run_dir / f"public_round_{round_no:02d}",
                test_paths=task.public_tests,
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

            if turn.problems():
                agent_problems.extend(
                    f"repair turn {round_no}: {p}" for p in turn.problems()
                )
                break

            if turn.thread_id and turn.thread_id != thread_id:
                raise RuntimeError(
                    "Codex resumed into a different thread; refusing invalid run."
                )

    changes = agent_change_stats(ws.agent_dir)
    if changes.get("files_changed") == 0:
        agent_problems.append("agent produced no file changes")

    # Held-out/original tests are restored only here and never fed back.
    final_ws = build_eval_workspace(task, ws, public_only=False)
    final_result, _, _ = evaluate(
        task,
        final_ws,
        timeout=test_timeout,
        log_prefix=run_dir / "final",
        test_paths=task.all_tests,
    )

    usage = Usage()
    for turn in turns:
        usage = usage + turn.usage

    null_row = load_null_baseline(results_root).get(project)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "timestamp_utc": stamp,
        "valid": not agent_problems,
        "agent_problems": agent_problems,
        "experiment": asdict(experiment),
        "environment": environment_metadata(),
        "config": {
            "model": model,
            "agent_timeout": agent_timeout,
            "test_timeout": test_timeout,
            "sandbox": "workspace-write",
        },
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
            "changes": changes,
        },
        "public_checks": [asdict(x) for x in public_results],
        "final": asdict(final_result),
        "null_baseline": null_row,
        "normalised_pass_rate": normalised_rate(
            final_result.passed, final_result.total, null_row
        ),
    }

    out = run_dir / "result.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    if agent_problems and strict:
        raise AgentUnavailable(
            f"{project}: {'; '.join(agent_problems)} "
            f"(run recorded at {out} and marked invalid)"
        )
    return out


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def load_results(results_root: str | Path) -> list[dict[str, Any]]:
    rows = []
    for p in Path(results_root).glob("*/*/result.json"):
        try:
            rows.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception:  # noqa: BLE001
            continue
    return rows


def _is_valid(row: dict[str, Any]) -> bool:
    # schema_version 1 predates validity tracking; treat those as valid.
    return bool(row.get("valid", True))


def summary_text(results_root: str | Path, include_invalid: bool = False) -> str:
    rows = load_results(results_root)
    if not rows:
        return "No results found."

    by_exp: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_exp.setdefault(row["experiment"]["name"], []).append(row)

    lines = []
    for name in EXPERIMENTS:
        group_all = by_exp.get(name, [])
        if not group_all:
            continue

        group = group_all if include_invalid else [
            r for r in group_all if _is_valid(r)
        ]
        invalid = len(group_all) - len(group)

        lines.append(f"{name}:")
        if invalid:
            lines.append(
                f"  INVALID RUNS EXCLUDED: {invalid}/{len(group_all)} "
                f"(agent did no work)"
            )
        if not group:
            lines.append("  no valid runs")
            continue

        successes = [bool(x["final"]["full_success"]) for x in group]
        rates = [
            x["final"]["pass_rate"]
            for x in group
            if x["final"]["pass_rate"] is not None
        ]
        norms = [
            x["normalised_pass_rate"]
            for x in group
            if x.get("normalised_pass_rate") is not None
        ]
        passed = sum(x["final"]["passed"] or 0 for x in group)
        total = sum(x["final"]["total"] or 0 for x in group)
        turns = [x["agent"]["turn_count"] for x in group]
        seconds = [x["agent"]["seconds"] for x in group]
        tokens = sum(
            x["agent"]["usage"]["input_tokens"]
            + x["agent"]["usage"]["output_tokens"]
            for x in group
        )

        lines.append(
            f"  success: {sum(successes)}/{len(group)} "
            f"({sum(successes)/len(group):.1%})"
        )
        lines.append(
            f"  mean test pass rate: {mean(rates):.1%}" if rates
            else "  mean test pass rate: n/a"
        )
        lines.append(
            f"  overall test pass rate: {passed}/{total} "
            f"({passed/total:.1%})" if total
            else "  overall test pass rate: n/a"
        )
        lines.append(
            f"  mean normalised pass rate: {mean(norms):.1%}" if norms
            else "  mean normalised pass rate: n/a "
                 "(run `migration-harness calibrate`)"
        )
        divergent = [
            x for x in group
            if x["final"].get("script_success") is not None
            and x["final"].get("script_success") != x["final"]["full_success"]
        ]
        if divergent:
            lines.append(
                f"  run_tests.sh disagreed with the fixed test list on "
                f"{len(divergent)} run(s): the script reported success while "
                f"declared benchmark tests failed"
            )
        lines.append(f"  mean agent turns: {mean(turns):.2f}")
        lines.append(f"  mean agent time: {mean(seconds):.1f}s")
        lines.append(f"  total tokens: {tokens:,}")

    return "\n".join(lines)


def export_csv(results_root: str | Path, output: str | Path) -> Path:
    rows = load_results(results_root)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "experiment", "project", "replicate", "valid", "agent_problems",
        "full_success", "script_success", "fixed_list_success",
        "pass_rate", "normalised_pass_rate",
        "passed", "failed", "total", "count_source",
        "null_passed", "null_total",
        "agent_turns", "agent_seconds",
        "files_changed", "lines_added", "lines_removed",
        "input_tokens", "cached_input_tokens", "output_tokens",
        "model", "harness_commit", "codex_version",
    ]
    with output.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for x in rows:
            final = x["final"]
            usage = x["agent"]["usage"]
            changes = x["agent"].get("changes") or {}
            env = x.get("environment") or {}
            nb = x.get("null_baseline") or {}
            w.writerow({
                "experiment": x["experiment"]["name"],
                "project": x["task"]["project"],
                "replicate": x["replicate"],
                "valid": _is_valid(x),
                "agent_problems": "; ".join(x.get("agent_problems") or []),
                "full_success": final["full_success"],
                "script_success": final.get("script_success"),
                "fixed_list_success": final.get("fixed_list_success"),
                "pass_rate": final["pass_rate"],
                "normalised_pass_rate": x.get("normalised_pass_rate"),
                "passed": final["passed"],
                "failed": final["failed"],
                "total": final["total"],
                "count_source": final.get("count_source"),
                "null_passed": nb.get("passed"),
                "null_total": nb.get("total"),
                "agent_turns": x["agent"]["turn_count"],
                "agent_seconds": x["agent"]["seconds"],
                "files_changed": changes.get("files_changed"),
                "lines_added": changes.get("lines_added"),
                "lines_removed": changes.get("lines_removed"),
                "input_tokens": usage["input_tokens"],
                "cached_input_tokens": usage["cached_input_tokens"],
                "output_tokens": usage["output_tokens"],
                "model": x.get("model"),
                "harness_commit": env.get("harness_commit"),
                "codex_version": env.get("codex_version"),
            })
    return output
