#!/usr/bin/env python3
"""
Runs the experiment ladder (baseline -> planning -> feedback -> gate) and writes
a detailed markdown report after every variant, plus a running cross-variant
comparison.

Resumable at the level of a single (experiment, project, replicate) key: only
missing keys are executed, so an interrupted variant is completed rather than
re-run. Duplicate keys are reported loudly instead of being averaged silently.

Validity comes from the harness itself (result["valid"] / ["agent_problems"]),
not from heuristics here.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

VARIANTS = ["baseline", "planning", "feedback", "gate"]

DESCRIPTIONS = {
    "baseline": "Single Codex migration pass with general instructions.",
    "planning": "Baseline plus mandatory repository analysis and component-level planning.",
    "feedback": "Planning plus one deterministic public-test repair round.",
    "gate": "Planning plus a public-test completion gate (up to 3 repair rounds).",
}

# Ordered: the first pattern that matches a line wins.
FAILURE_PATTERNS = [
    ("timeout",                r"HARNESS_TEST_TIMEOUT|HARNESS_AGENT_TIMEOUT"),
    ("invalid python",         r"\b(SyntaxError|IndentationError|TabError)\b"),
    ("import / layout",        r"\b(ModuleNotFoundError|ImportError)\b|cannot import name"),
    ("missing attribute/API",  r"\bAttributeError\b"),
    ("signature mismatch",     r"\bTypeError\b"),
    ("missing definition",     r"\bNameError\b"),
    ("wrong key/index",        r"\b(KeyError|IndexError)\b"),
    ("wrong value",            r"\b(ValueError|ArithmeticError|ZeroDivisionError)\b"),
    ("wrong behaviour",        r"\bAssertionError\b|^E\s+assert"),
]


# --------------------------------------------------------------------- utils

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sh(cmd: list[str]) -> str:
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        ).stdout.strip().splitlines()[0]
    except Exception:  # noqa: BLE001
        return "unknown"


def read_tasks(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def fmt_pct(x) -> str:
    return "n/a" if x is None else f"{x:.1%}"


def fmt_int(x) -> str:
    return "n/a" if x is None else f"{x:,}"


# ------------------------------------------------------------- result model

def load_variant(results: Path, variant: str, null: dict) -> tuple[list[dict], list[str]]:
    """
    Returns (rows, duplicate_keys).

    Validity is taken from the harness's own verdict. Normalised pass rate is
    taken from the result when present, and only computed here as a fallback
    for results written before the harness recorded it.
    """
    by_key: dict[tuple[str, int], list[dict]] = defaultdict(list)

    for rp in sorted((results / variant).glob("*/result.json")):
        try:
            r = json.loads(rp.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue

        f, a = r["final"], r["agent"]
        proj = r["task"]["project"]
        replicate = int(r.get("replicate", 1))

        problems = list(r.get("agent_problems") or [])
        valid = bool(r.get("valid", not problems))

        norm = r.get("normalised_pass_rate")
        if norm is None:
            # null_baseline.json stores each project's figures directly.
            nb = null.get(proj) or {}
            np_ = nb.get("passed")
            if np_ is not None and f.get("passed") is not None and f.get("total"):
                denominator = f["total"] - np_
                if denominator > 0:
                    norm = (f["passed"] - np_) / denominator

        by_key[(proj, replicate)].append({
            "project": proj, "replicate": replicate, "run_dir": rp.parent,
            "timestamp": r.get("timestamp_utc", ""),
            "passed": f.get("passed"), "total": f.get("total"),
            "pass_rate": f.get("pass_rate"), "normalised": norm,
            "success": bool(f.get("full_success")),
            "script_success": f.get("script_success"),
            "turns": a.get("turn_count", 0), "seconds": a.get("seconds", 0.0),
            "tokens": a["usage"]["input_tokens"] + a["usage"]["output_tokens"],
            "files_changed": (a.get("changes") or {}).get("files_changed"),
            "public_checks": r.get("public_checks", []),
            "final_message": (a["turns"][-1].get("final_message") or "").strip()
            if a.get("turns") else "",
            "valid": valid, "problems": problems,
        })

    rows, duplicates = [], []
    for key, group in sorted(by_key.items()):
        if len(group) > 1:
            duplicates.append(f"{key[0]} r{key[1]} ({len(group)} runs)")
        # Keep the newest run for a duplicated key; the duplicate is reported.
        rows.append(sorted(group, key=lambda x: x["timestamp"])[-1])
    return rows, duplicates


def missing_keys(rows: list[dict], projects: list[str], replicates: int) -> list[tuple[str, int]]:
    have = {(r["project"], r["replicate"]) for r in rows if r["valid"]}
    return [
        (p, rep)
        for rep in range(1, replicates + 1)
        for p in projects
        if (p, rep) not in have
    ]


def classify(run_dir: Path) -> tuple[Counter, list[str]]:
    text = ""
    for name in ("final.stdout.txt", "final.stderr.txt",
                 "final_count.stdout.txt", "final_count.stderr.txt"):
        p = run_dir / name
        if p.exists():
            text += p.read_text(encoding="utf-8", errors="replace") + "\n"

    cats, samples = Counter(), []
    for line in text.splitlines():
        for label, pat in FAILURE_PATTERNS:
            if re.search(pat, line):
                cats[label] += 1
                if len(samples) < 6 and line.strip():
                    samples.append(line.strip()[:160])
                break

    named = re.findall(r"^(?:FAILED|ERROR)\s+(\S+)", text, flags=re.MULTILINE)
    if named:
        samples = list(dict.fromkeys(named))[:8] + samples[:2]
    return cats, samples


def agg(rows: list[dict]) -> dict:
    ok = [r for r in rows if r["valid"]]
    rates = [r["pass_rate"] for r in ok if r["pass_rate"] is not None]
    norms = [r["normalised"] for r in ok if r["normalised"] is not None]
    tp = sum(r["passed"] or 0 for r in ok)
    tt = sum(r["total"] or 0 for r in ok)
    return {
        "n": len(rows), "valid": len(ok),
        "success": sum(1 for r in ok if r["success"]),
        "macro": statistics.mean(rates) if rates else None,
        "micro": (tp / tt) if tt else None,
        "micro_str": f"{tp}/{tt}",
        "norm": statistics.mean(norms) if norms else None,
        "norm_n": len(norms),
        "turns": statistics.mean([r["turns"] for r in ok]) if ok else None,
        "seconds": statistics.mean([r["seconds"] for r in ok]) if ok else None,
        "tokens": sum(r["tokens"] for r in ok),
    }


# ---------------------------------------------------------------- reporting

def write_variant_report(results: Path, variant: str, rows: list[dict],
                         meta: dict, prev: tuple[str, dict] | None,
                         duplicates: list[str]) -> Path:
    a = agg(rows)
    L: list[str] = []
    L.append(f"# {variant.capitalize()}")
    L.append("")
    L.append(DESCRIPTIONS.get(variant, ""))
    L.append("")
    L.append("| Setting | Value |")
    L.append("|---|---|")
    for k, v in meta.items():
        L.append(f"| {k} | {v} |")
    L.append("")

    if duplicates:
        L.append("> **DUPLICATE RUNS DETECTED — results below use the newest "
                 "run for each key, but this must be resolved before "
                 "publishing.**")
        L.append(">")
        for d in duplicates:
            L.append(f"> - {d}")
        L.append("")

    L.append("## Per-project results")
    L.append("")
    L.append("| Project | Rep | Passed | Total | Pass rate | Normalised | "
             "Success | Turns | Files | Tokens | Time |")
    L.append("|---|--:|--:|--:|--:|--:|:--:|--:|--:|--:|--:|")
    for r in sorted(rows, key=lambda x: (x["project"], x["replicate"])):
        flag = " ⚠️" if not r["valid"] else ""
        L.append(
            f"| {r['project']}{flag} | {r['replicate']} | {r['passed']} | {r['total']} | "
            f"{fmt_pct(r['pass_rate'])} | {fmt_pct(r['normalised'])} | "
            f"{'yes' if r['success'] else 'no'} | {r['turns']} | "
            f"{r['files_changed'] if r['files_changed'] is not None else '?'} | "
            f"{fmt_int(r['tokens'])} | {r['seconds']:.0f}s |"
        )
    L.append("")

    bad = [r for r in rows if not r["valid"]]
    if bad:
        L.append("> ⚠️ **Invalid runs — excluded from the aggregates below.**")
        L.append(">")
        for r in bad:
            L.append(f"> - `{r['project']}` r{r['replicate']}: "
                     f"{', '.join(r['problems']) or 'marked invalid by the harness'}")
        L.append("")

    divergent = [
        r for r in rows
        if r["script_success"] is not None and r["script_success"] != r["success"]
    ]
    if divergent:
        L.append("> **run_tests.sh disagreed with the fixed test list** on "
                 + ", ".join(f"`{r['project']}`" for r in divergent)
                 + " — the benchmark script reported success while declared "
                   "tests failed. The stricter verdict is used.")
        L.append("")

    L.append("## Aggregate")
    L.append("")
    L.append(f"- Valid runs: **{a['valid']}/{a['n']}**")
    if a["valid"]:
        L.append(f"- Full migration success: **{a['success']}/{a['valid']}** "
                 f"({a['success']/a['valid']:.1%})")
    L.append(f"- Mean project pass rate (macro): **{fmt_pct(a['macro'])}**")
    L.append(f"- Overall test pass rate (micro): **{fmt_pct(a['micro'])}** ({a['micro_str']})")
    L.append(
        f"- Mean normalised pass rate: **{fmt_pct(a['norm'])}** "
        f"(over {a['norm_n']} project(s) that carry signal) — corrected for "
        f"tests that pass without any implementation"
    )
    if a["turns"] is not None:
        L.append(f"- Mean agent turns: {a['turns']:.2f}")
        L.append(f"- Mean agent time: {a['seconds']:.0f}s")
    L.append(f"- Total tokens: {fmt_int(a['tokens'])}")
    L.append("")

    if prev:
        pname, pa = prev
        L.append(f"## Change vs `{pname}`")
        L.append("")
        L.append(f"| Metric | {pname} | {variant} | Δ |")
        L.append("|---|--:|--:|--:|")
        if pa["valid"] and a["valid"]:
            sx, sy = pa["success"] / pa["valid"], a["success"] / a["valid"]
            L.append(f"| Full success | {sx:.1%} | {sy:.1%} | {sy - sx:+.1%} |")
        for label, key in (
            ("Pass rate (macro)", "macro"),
            ("Pass rate (micro)", "micro"),
            ("Normalised pass rate", "norm"),
        ):
            x, y = pa.get(key), a.get(key)
            if x is None or y is None:
                L.append(f"| {label} | {fmt_pct(x)} | {fmt_pct(y)} | n/a |")
            else:
                L.append(f"| {label} | {x:.1%} | {y:.1%} | {y - x:+.1%} |")
        if pa["turns"] is not None and a["turns"] is not None:
            L.append(f"| Mean turns | {pa['turns']:.2f} | {a['turns']:.2f} | "
                     f"{a['turns'] - pa['turns']:+.2f} |")
        L.append("")

    if variant in ("feedback", "gate"):
        L.append("## Repair activity")
        L.append("")
        L.append("| Project | Turns | Public check progression | Repair fired |")
        L.append("|---|--:|---|:--:|")
        for r in sorted(rows, key=lambda x: x["project"]):
            prog = " → ".join(
                f"{c.get('passed')}/{c.get('total')}" for c in r["public_checks"]
            ) or "—"
            L.append(f"| {r['project']} | {r['turns']} | {prog} | "
                     f"{'yes' if r['turns'] > 1 else 'no'} |")
        L.append("")

    L.append("## Failure analysis")
    L.append("")
    failing = [r for r in rows if r["valid"] and not r["success"]]
    if not failing:
        L.append("No failing projects among valid runs.")
        L.append("")
    for r in sorted(failing, key=lambda x: x["pass_rate"] or 0):
        cats, samples = classify(r["run_dir"])
        L.append(f"### {r['project']} — {r['passed']}/{r['total']} ({fmt_pct(r['pass_rate'])})")
        L.append("")
        L.append("Failure categories: " + (
            ", ".join(f"**{k}** ×{v}" for k, v in cats.most_common())
            or "not classifiable from test output."
        ))
        L.append("")
        if samples:
            L.append("```")
            L.extend(samples)
            L.append("```")
            L.append("")
        L.append("*Interpretation:* ")
        L.append("")

    L.append("## Next iteration")
    L.append("")
    L.append("*Hypothesis motivated by the failures above:* ")
    L.append("")
    L.append(f"<sub>Generated {now()}</sub>")

    out = results / "reports" / f"{variant}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


def write_comparison(results: Path, done: list[tuple[str, dict, list[dict]]]) -> Path:
    L = ["# Experiment comparison", "",
         "All variants run on the same task list, model and timeouts.", "",
         "| Variant | Valid | Full success | Pass rate (macro) | "
         "Pass rate (micro) | Normalised | Mean turns | Mean time | Tokens |",
         "|---|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for name, a, _ in done:
        succ = (f"{a['success']}/{a['valid']} ({a['success']/a['valid']:.0%})"
                if a["valid"] else "n/a")
        turns = f"{a['turns']:.2f}" if a["turns"] is not None else "n/a"
        secs = f"{a['seconds']:.0f}s" if a["seconds"] is not None else "n/a"
        L.append(
            f"| **{name}** | {a['valid']}/{a['n']} | {succ} | {fmt_pct(a['macro'])} | "
            f"{fmt_pct(a['micro'])} | {fmt_pct(a['norm'])} | {turns} | {secs} | "
            f"{fmt_int(a['tokens'])} |"
        )
    L.append("")

    if len(done) > 1:
        for label, key in (("pass rate", "pass_rate"), ("normalised pass rate", "normalised")):
            L.append(f"## Per-project {label} by variant")
            L.append("")
            projects = sorted({r["project"] for _, _, rows in done for r in rows})
            L.append("| Project | " + " | ".join(n for n, _, _ in done) + " |")
            L.append("|---" * (len(done) + 1) + "|")
            for p in projects:
                cells = []
                for _, _, rows in done:
                    m = [r for r in rows if r["project"] == p]
                    cells.append(fmt_pct(m[0][key]) if m else "—")
                L.append(f"| {p} | " + " | ".join(cells) + " |")
            L.append("")

    L.append("## Attribution")
    L.append("")
    for i in range(1, len(done)):
        pn, pa, _ = done[i - 1]
        cn, ca, _ = done[i]
        parts = []
        if pa["macro"] is not None and ca["macro"] is not None:
            parts.append(f"macro pass rate {ca['macro'] - pa['macro']:+.1%}")
        if pa["norm"] is not None and ca["norm"] is not None:
            parts.append(f"normalised {ca['norm'] - pa['norm']:+.1%}")
        parts.append(f"full success {pa['success']}/{pa['valid']} → "
                     f"{ca['success']}/{ca['valid']}")
        L.append(f"- **{pn} → {cn}**: " + ", ".join(parts) + ". *Explanation:* ")
    if any(n == "gate" for n, _, _ in done):
        L.append("")
        L.append("> Note: `feedback → gate` changes two things at once — the "
                 "number of repair rounds (1 → 3) *and* the completion-gate "
                 "wording. Treat it as a combined intervention.")
    L.append("")
    L.append(f"<sub>Generated {now()}</sub>")

    out = results / "reports" / "COMPARISON.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    return out


# --------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--tasks", required=True)
    ap.add_argument("--results", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--source", default="Java")
    ap.add_argument("--target", default="Python")
    ap.add_argument("--variants", default=",".join(VARIANTS))
    ap.add_argument("--agent-timeout", type=int, default=1800)
    ap.add_argument("--test-timeout", type=int, default=900)
    ap.add_argument("--replicates", type=int, default=1)
    ap.add_argument("--force", action="store_true",
                    help="Run every key again, adding replicates rather than "
                         "resuming. Rarely what you want.")
    ap.add_argument("--always-gate", action="store_true")
    ap.add_argument("--report-only", action="store_true",
                    help="Regenerate reports from existing results; run nothing.")
    args = ap.parse_args()

    results = Path(args.results).expanduser().resolve()
    tasks_file = Path(args.tasks).expanduser().resolve()
    projects = read_tasks(tasks_file)
    wanted = [v.strip() for v in args.variants.split(",") if v.strip()]

    null_path = results / "null_baseline.json"
    null: dict = {}
    if null_path.exists():
        try:
            null = json.loads(null_path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            null = {}

    if not null and not args.report_only:
        print("ERROR: no null_baseline.json in the results directory.\n"
              "Run this first (it needs no agent credits):\n\n"
              f"  migration-harness calibrate --dataset {args.dataset} "
              f"--tasks {tasks_file} --results {results}\n", file=sys.stderr)
        return 4

    meta_base = {
        "Model": args.model,
        "Codex CLI": sh(["codex", "--version"]) if shutil.which("codex") else "n/a",
        "Harness commit": sh(["git", "rev-parse", "--short", "HEAD"]),
        "Migration": f"{args.source} → {args.target}",
        "Tasks": f"{len(projects)} ({tasks_file.name})",
        "Agent timeout": f"{args.agent_timeout}s",
        "Test timeout": f"{args.test_timeout}s",
        "Replicates": args.replicates,
        "Null-agent calibration": "loaded" if null else "MISSING",
    }

    print("=" * 74)
    print("EXPERIMENT LADDER")
    for k, v in meta_base.items():
        print(f"  {k:<26s}: {v}")
    print(f"  {'Variants':<26s}: {' -> '.join(wanted)}")
    print(f"  {'Projects':<26s}: {', '.join(projects)}")
    print("=" * 74)
    print()

    if not args.report_only:
        print("Checking the agent is usable...")
        probe = subprocess.run(
            ["migration-harness", "probe", "--model", args.model],
            capture_output=True, text=True,
        )
        if probe.returncode != 0:
            print(f"\nABORT: {probe.stderr.strip() or probe.stdout.strip()}",
                  file=sys.stderr)
            print("Nothing was executed.", file=sys.stderr)
            return 2
        print("  agent OK\n")

    done: list[tuple[str, dict, list[dict]]] = []

    for variant in wanted:
        if variant == "gate" and not args.always_gate and not args.report_only:
            fb = [d for d in done if d[0] == "feedback"]
            if fb and fb[0][1]["valid"] and fb[0][1]["success"] == fb[0][1]["valid"]:
                print("SKIP gate: feedback already achieved full success on "
                      "every project, so the completion gate has nothing to "
                      "demonstrate. (--always-gate overrides)\n")
                continue

        rows, duplicates = load_variant(results, variant, null)
        todo = [] if args.report_only else (
            [(p, rep) for rep in range(1, args.replicates + 1) for p in projects]
            if args.force else missing_keys(rows, projects, args.replicates)
        )

        if todo:
            print(f"== {variant}: {len(todo)} migration(s) to run "
                  f"({len(rows)} already present) ==\n", flush=True)
        else:
            print(f"== {variant}: complete ({len(rows)} runs) — reporting only ==")

        aborted = False
        for project, replicate in todo:
            print(f"-- {variant} | {project} | replicate {replicate} --", flush=True)
            rc = subprocess.run([
                "migration-harness", "run",
                "--dataset", args.dataset,
                "--source", args.source, "--target", args.target,
                "--project", project,
                "--experiment", variant,
                "--model", args.model,
                "--results", str(results),
                "--replicate", str(replicate),
                "--agent-timeout", str(args.agent_timeout),
                "--test-timeout", str(args.test_timeout),
            ]).returncode
            if rc == 2:
                print("\nABORT: the agent stopped working (quota, auth or "
                      "crash). Remaining runs were not started.\n"
                      "Re-run this script when it is available — completed "
                      "runs are skipped automatically.", file=sys.stderr)
                aborted = True
                break

        rows, duplicates = load_variant(results, variant, null)
        prev = (done[-1][0], done[-1][1]) if done else None
        meta = dict(meta_base, **{"Variant": variant, "Report generated": now()})
        rep = write_variant_report(results, variant, rows, meta, prev, duplicates)
        a = agg(rows)
        done.append((variant, a, rows))
        comp = write_comparison(results, done)

        print()
        print("-" * 74)
        print(f"{variant.upper()}: {a['success']}/{a['valid']} full success | "
              f"macro {fmt_pct(a['macro'])} | micro {fmt_pct(a['micro'])} | "
              f"normalised {fmt_pct(a['norm'])}")
        if duplicates:
            print(f"  DUPLICATE KEYS: {', '.join(duplicates)}")
        print(f"  report     : {rep}")
        print(f"  comparison : {comp}")
        print("-" * 74)
        print()

        if aborted:
            return 3
        if duplicates:
            print("ERROR: duplicate (project, replicate) keys found. Remove the "
                  "extra run directories before publishing these numbers.",
                  file=sys.stderr)
            return 5

    subprocess.run(["migration-harness", "summary",
                    "--results", str(results),
                    "--csv", str(results / "results.csv")], check=False)

    print()
    print("=" * 74)
    print("STUDY COMPLETE")
    print(f"  reports    : {results / 'reports'}")
    print(f"  comparison : {results / 'reports' / 'COMPARISON.md'}")
    print(f"  csv        : {results / 'results.csv'}")
    print("=" * 74)
    print()
    print("Each report has blank *Interpretation:* and *Hypothesis:* lines.")
    print("Fill those in — that prose is what the task actually grades.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
