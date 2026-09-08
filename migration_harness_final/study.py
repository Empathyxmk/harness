#!/usr/bin/env python3
"""
Runs the full experiment ladder (baseline -> planning -> feedback -> gate) and
writes a detailed markdown report after every variant, plus a running
cross-variant comparison.

Safe to re-run: variants that already completed are reported, not re-run.
Stops the moment the agent becomes unusable (quota, auth, crash) instead of
filling the results directory with empty runs.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import Counter
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
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=30).stdout.strip()
    except Exception:
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


# ----------------------------------------------------------- agent liveness

def probe_agent(model: str) -> tuple[bool, str]:
    """One cheap Codex call under the same conditions the real runs use."""
    d = Path(tempfile.mkdtemp(prefix="probe_"))
    try:
        subprocess.run(["git", "init", "-q"], cwd=d, capture_output=True)
        p = subprocess.run(
            ["codex", "-a", "never", "exec", "--sandbox", "workspace-write",
             "--json", "--model", model, "Reply with exactly: PROBE_OK"],
            cwd=d, capture_output=True, text=True, timeout=180,
            stdin=subprocess.DEVNULL,
        )
        out = (p.stdout or "") + "\n" + (p.stderr or "")
        for raw in out.splitlines():
            raw = raw.strip()
            if not raw.startswith("{"):
                continue
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if ev.get("type") in ("error", "turn.failed"):
                msg = ev.get("message") or (ev.get("error") or {}).get("message", "")
                return False, str(msg)
            if ev.get("type") == "turn.completed":
                return True, "ok"
        return False, (out.strip()[-500:] or f"no turn.completed (exit {p.returncode})")
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"
    finally:
        shutil.rmtree(d, ignore_errors=True)


def run_error(run_dir: Path) -> str | None:
    """Return an error message if the agent failed during this run."""
    for log in sorted((run_dir / "agent_logs").glob("*.jsonl")):
        for raw in log.read_text(encoding="utf-8", errors="replace").splitlines():
            raw = raw.strip()
            if not raw.startswith("{"):
                continue
            try:
                ev = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if ev.get("type") in ("error", "turn.failed"):
                m = ev.get("message") or (ev.get("error") or {}).get("message", "")
                return str(m)[:300]
    return None


# ------------------------------------------------------------- result model

def load_variant(results: Path, variant: str, null: dict | None) -> list[dict]:
    rows = []
    for rp in sorted((results / variant).glob("*/result.json")):
        try:
            r = json.loads(rp.read_text(encoding="utf-8"))
        except Exception:
            continue
        run = rp.parent
        f, a = r["final"], r["agent"]
        proj = r["task"]["project"]

        err = run_error(run)
        invalid = []
        if a["turns"][0]["return_code"] != 0:
            invalid.append(f"agent exit {a['turns'][0]['return_code']}")
        if a["usage"]["input_tokens"] == 0:
            invalid.append("0 tokens")
        if a["seconds"] < 30:
            invalid.append(f"{a['seconds']:.0f}s agent time")
        if err:
            invalid.append(f"agent error: {err}")

        norm = None
        if null and proj in null and f["passed"] is not None and f["total"]:
            nb = null[proj].get("null_baseline", {})
            np_ = nb.get("passed")
            if np_ is not None and (f["total"] - np_) > 0:
                norm = (f["passed"] - np_) / (f["total"] - np_)

        rows.append({
            "project": proj, "run_dir": run,
            "passed": f["passed"], "total": f["total"],
            "pass_rate": f["pass_rate"], "normalised": norm,
            "success": bool(f["full_success"]),
            "turns": a["turn_count"], "seconds": a["seconds"],
            "tokens": a["usage"]["input_tokens"] + a["usage"]["output_tokens"],
            "public_checks": r.get("public_checks", []),
            "final_message": (a["turns"][-1].get("final_message") or "").strip(),
            "invalid": invalid,
        })
    return rows


def classify(run_dir: Path) -> tuple[Counter, list[str]]:
    text = ""
    for name in ("final.stdout.txt", "final.stderr.txt"):
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
        samples = [f"{n}" for n in dict.fromkeys(named)][:8] + samples[:2]
    return cats, samples


def agg(rows: list[dict]) -> dict:
    ok = [r for r in rows if not r["invalid"]]
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
        "turns": statistics.mean([r["turns"] for r in ok]) if ok else None,
        "seconds": statistics.mean([r["seconds"] for r in ok]) if ok else None,
        "tokens": sum(r["tokens"] for r in ok),
    }


# ---------------------------------------------------------------- reporting

def write_variant_report(results: Path, variant: str, rows: list[dict],
                         meta: dict, prev: tuple[str, dict] | None) -> Path:
    a = agg(rows)
    L = []
    L.append(f"# {variant.capitalize()}")
    L.append("")
    L.append(DESCRIPTIONS.get(variant, ""))
    L.append("")
    L.append("| Setting | Value |")
    L.append("|---|---|")
    for k, v in meta.items():
        L.append(f"| {k} | {v} |")
    L.append("")

    L.append("## Per-project results")
    L.append("")
    L.append("| Project | Passed | Total | Pass rate | Normalised | Success | Turns | Tokens | Time |")
    L.append("|---|--:|--:|--:|--:|:--:|--:|--:|--:|")
    for r in sorted(rows, key=lambda x: x["project"]):
        flag = " ⚠️" if r["invalid"] else ""
        L.append(
            f"| {r['project']}{flag} | {r['passed']} | {r['total']} | "
            f"{fmt_pct(r['pass_rate'])} | {fmt_pct(r['normalised'])} | "
            f"{'yes' if r['success'] else 'no'} | {r['turns']} | "
            f"{fmt_int(r['tokens'])} | {r['seconds']:.0f}s |"
        )
    L.append("")

    bad = [r for r in rows if r["invalid"]]
    if bad:
        L.append("> ⚠️ **Invalid runs — excluded from the aggregates below.**")
        L.append(">")
        for r in bad:
            L.append(f"> - `{r['project']}`: {', '.join(r['invalid'])}")
        L.append("")

    L.append("## Aggregate")
    L.append("")
    L.append(f"- Valid runs: **{a['valid']}/{a['n']}**")
    L.append(f"- Full migration success: **{a['success']}/{a['valid']}** "
             f"({(a['success']/a['valid']) if a['valid'] else 0:.1%})")
    L.append(f"- Mean project pass rate (macro): **{fmt_pct(a['macro'])}**")
    L.append(f"- Overall test pass rate (micro): **{fmt_pct(a['micro'])}** ({a['micro_str']})")
    if a["norm"] is not None:
        L.append(f"- Mean normalised pass rate: **{fmt_pct(a['norm'])}** "
                 f"— corrected for tests that pass without any implementation")
    L.append(f"- Mean agent turns: {a['turns']:.2f}" if a["turns"] else "- Mean agent turns: n/a")
    L.append(f"- Mean agent time: {a['seconds']:.0f}s" if a["seconds"] else "- Mean agent time: n/a")
    L.append(f"- Total tokens: {fmt_int(a['tokens'])}")
    L.append("")

    if prev:
        pname, pa = prev
        L.append(f"## Change vs `{pname}`")
        L.append("")
        L.append(f"| Metric | {pname} | {variant} | Δ |")
        L.append("|---|--:|--:|--:|")

        def delta(label, key, pct=True):
            x, y = pa.get(key), a.get(key)
            if x is None or y is None:
                L.append(f"| {label} | n/a | n/a | n/a |")
                return
            d = y - x
            s = f"{d:+.1%}" if pct else f"{d:+.2f}"
            L.append(f"| {label} | {fmt_pct(x) if pct else f'{x:.2f}'} | "
                     f"{fmt_pct(y) if pct else f'{y:.2f}'} | {s} |")

        sx = (pa["success"] / pa["valid"]) if pa["valid"] else None
        sy = (a["success"] / a["valid"]) if a["valid"] else None
        if sx is not None and sy is not None:
            L.append(f"| Full success | {sx:.1%} | {sy:.1%} | {sy - sx:+.1%} |")
        delta("Pass rate (macro)", "macro")
        delta("Pass rate (micro)", "micro")
        delta("Normalised pass rate", "norm")
        delta("Mean turns", "turns", pct=False)
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
    failing = [r for r in rows if not r["success"] and not r["invalid"]]
    if not failing:
        L.append("No failing projects among valid runs.")
        L.append("")
    for r in sorted(failing, key=lambda x: x["pass_rate"] or 0):
        cats, samples = classify(r["run_dir"])
        L.append(f"### {r['project']} — {r['passed']}/{r['total']} ({fmt_pct(r['pass_rate'])})")
        L.append("")
        if cats:
            L.append("Failure categories: " +
                     ", ".join(f"**{k}** ×{v}" for k, v in cats.most_common()))
        else:
            L.append("Failure categories: not classifiable from test output.")
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
         "All variants run on the same task list, model and timeouts.", ""]
    L.append("| Variant | Valid | Full success | Pass rate (macro) | Pass rate (micro) | Normalised | Mean turns | Mean time | Tokens |")
    L.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
    for name, a, _ in done:
        succ = f"{a['success']}/{a['valid']}" + (
            f" ({a['success']/a['valid']:.0%})" if a["valid"] else "")
        L.append(
            f"| **{name}** | {a['valid']}/{a['n']} | {succ} | {fmt_pct(a['macro'])} | "
            f"{fmt_pct(a['micro'])} | {fmt_pct(a['norm'])} | "
            f"{a['turns']:.2f} | {a['seconds']:.0f}s | {fmt_int(a['tokens'])} |"
            if a["turns"] and a["seconds"] else
            f"| **{name}** | {a['valid']}/{a['n']} | {succ} | {fmt_pct(a['macro'])} | "
            f"{fmt_pct(a['micro'])} | {fmt_pct(a['norm'])} | n/a | n/a | {fmt_int(a['tokens'])} |"
        )
    L.append("")

    if len(done) > 1:
        L.append("## Per-project pass rate by variant")
        L.append("")
        projects = sorted({r["project"] for _, _, rows in done for r in rows})
        L.append("| Project | " + " | ".join(n for n, _, _ in done) + " |")
        L.append("|---" * (len(done) + 1) + "|")
        for p in projects:
            cells = []
            for _, _, rows in done:
                m = [r for r in rows if r["project"] == p]
                cells.append(fmt_pct(m[0]["pass_rate"]) if m else "—")
            L.append(f"| {p} | " + " | ".join(cells) + " |")
        L.append("")

    L.append("## Attribution")
    L.append("")
    for i in range(1, len(done)):
        pn, pa, _ = done[i - 1]
        cn, ca, _ = done[i]
        if pa["macro"] is not None and ca["macro"] is not None:
            d = ca["macro"] - pa["macro"]
            L.append(f"- **{pn} → {cn}**: macro pass rate {d:+.1%}, "
                     f"full success {pa['success']}/{pa['valid']} → {ca['success']}/{ca['valid']}. "
                     f"*Explanation:* ")
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
                    help="re-run variants that already have complete results")
    ap.add_argument("--always-gate", action="store_true",
                    help="run gate even if feedback already saturated")
    args = ap.parse_args()

    results = Path(args.results).expanduser().resolve()
    tasks_file = Path(args.tasks).expanduser().resolve()
    tasks = read_tasks(tasks_file)
    wanted = [v.strip() for v in args.variants.split(",") if v.strip()]

    null = None
    nb = results / "null_baseline.json"
    if nb.exists():
        try:
            null = json.loads(nb.read_text(encoding="utf-8"))
        except Exception:
            null = None

    meta_base = {
        "Model": args.model,
        "Codex CLI": sh(["codex", "--version"]).splitlines()[0] if shutil.which("codex") else "n/a",
        "Harness commit": sh(["git", "rev-parse", "--short", "HEAD"]),
        "Migration": f"{args.source} → {args.target}",
        "Tasks": f"{len(tasks)} ({tasks_file.name})",
        "Agent timeout": f"{args.agent_timeout}s",
        "Test timeout": f"{args.test_timeout}s",
        "Replicates": args.replicates,
        "Null-agent calibration": "loaded" if null else "not available",
    }

    print("=" * 72)
    print("EXPERIMENT LADDER")
    for k, v in meta_base.items():
        print(f"  {k:<26s}: {v}")
    print(f"  {'Variants':<26s}: {' -> '.join(wanted)}")
    print(f"  {'Projects':<26s}: {', '.join(tasks)}")
    print("=" * 72)
    print()

    print("Checking the agent is usable...")
    ok, msg = probe_agent(args.model)
    if not ok:
        print(f"\nABORT: the agent cannot run right now.\n  {msg}\n", file=sys.stderr)
        print("Nothing was executed. Re-run this script when it is available.",
              file=sys.stderr)
        return 2
    print("  agent OK\n")

    done: list[tuple[str, dict, list[dict]]] = []

    for variant in wanted:
        expected = len(tasks) * args.replicates
        existing = load_variant(results, variant, null)
        complete = len(existing) >= expected and not any(r["invalid"] for r in existing)

        if variant == "gate" and not args.always_gate and done:
            fb = [d for d in done if d[0] == "feedback"]
            if fb and fb[0][1]["valid"] and fb[0][1]["success"] == fb[0][1]["valid"]:
                print("SKIP gate: feedback already achieved full success on every "
                      "project, so the completion gate has nothing to demonstrate.")
                print("      (use --always-gate to run it anyway)\n")
                continue

        if complete and not args.force:
            print(f"== {variant}: already complete ({len(existing)} runs) — reporting only ==")
            rows = existing
        else:
            print(f"== {variant}: running {expected} migration(s) ==\n", flush=True)
            cmd = [
                "migration-harness", "batch",
                "--dataset", args.dataset,
                "--source", args.source, "--target", args.target,
                "--tasks", str(tasks_file),
                "--experiment", variant,
                "--model", args.model,
                "--results", str(results),
                "--agent-timeout", str(args.agent_timeout),
                "--test-timeout", str(args.test_timeout),
                "--replicates", str(args.replicates),
            ]
            rc = subprocess.run(cmd).returncode
            rows = load_variant(results, variant, null)
            if rc != 0:
                print(f"\nWARNING: batch exited {rc}", file=sys.stderr)

        prev = (done[-1][0], done[-1][1]) if done else None
        meta = dict(meta_base, **{"Variant": variant, "Report generated": now()})
        rep = write_variant_report(results, variant, rows, meta, prev)
        a = agg(rows)
        done.append((variant, a, rows))
        comp = write_comparison(results, done)

        print()
        print("-" * 72)
        print(f"{variant.upper()}: {a['success']}/{a['valid']} full success | "
              f"macro {fmt_pct(a['macro'])} | micro {fmt_pct(a['micro'])} | "
              f"normalised {fmt_pct(a['norm'])}")
        print(f"  report     : {rep}")
        print(f"  comparison : {comp}")
        print("-" * 72)
        print()

        broken = [r for r in rows if r["invalid"]]
        if broken:
            print("ABORT: the agent stopped working during this variant:",
                  file=sys.stderr)
            for r in broken:
                print(f"  {r['project']}: {', '.join(r['invalid'])}", file=sys.stderr)
            print("\nRemaining variants were not started. Fix the agent (usually "
                  "waiting for quota) and re-run this script — completed variants "
                  "are skipped automatically.", file=sys.stderr)
            return 3

    try:
        subprocess.run(["migration-harness", "summary",
                        "--results", str(results),
                        "--csv", str(results / "results.csv")], check=False)
    except Exception:
        pass

    print()
    print("=" * 72)
    print("STUDY COMPLETE")
    print(f"  reports    : {results / 'reports'}")
    print(f"  comparison : {results / 'reports' / 'COMPARISON.md'}")
    print(f"  csv        : {results / 'results.csv'}")
    print("=" * 72)
    print()
    print("Each report has blank *Interpretation:* and *Hypothesis:* lines.")
    print("Fill those in — that prose is what the task actually grades.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
