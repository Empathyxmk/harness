#!/usr/bin/env bash
# Formal baseline over tasks_formal.txt, with the checks that would have caught
# the last run. Aborts before spending credits if the agent cannot actually run,
# and refuses to report a number for any task where the agent did no work.
set -euo pipefail

HARNESS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATASET="$HOME/projects/Harness/RepoTransBench"
TASKS="$HARNESS_DIR/tasks_formal.txt"
RESULTS="$HARNESS_DIR/results_formal"
MODEL="gpt-5.6-terra"

cd "$HARNESS_DIR"

# ---------------------------------------------------------------- preflight
[[ -f .venv/bin/activate ]] || { echo "ERROR: no .venv in $HARNESS_DIR" >&2; exit 1; }
# shellcheck disable=SC1091
source .venv/bin/activate

[[ -f "$TASKS" ]] || { echo "ERROR: missing $TASKS" >&2; exit 1; }
[[ -d "$DATASET/source_projects" && -d "$DATASET/target_projects" ]] \
    || { echo "ERROR: bad dataset: $DATASET" >&2; exit 1; }
command -v migration-harness >/dev/null || { echo "ERROR: migration-harness not installed" >&2; exit 1; }
command -v pytest            >/dev/null || { echo "ERROR: pytest not on PATH" >&2; exit 1; }
command -v codex             >/dev/null || { echo "ERROR: codex not on PATH" >&2; exit 1; }

echo "Formal baseline"
echo "  harness : $HARNESS_DIR"
echo "  dataset : $DATASET"
echo "  results : $RESULTS"
echo "  model   : $MODEL"
echo "  codex   : $(codex --version 2>&1 | head -1)"
echo
echo "Tasks:"
sed '/^[[:space:]]*$/d; /^[[:space:]]*#/d' "$TASKS" | sed 's/^/  /'
echo

# --- live agent probe: fail here, not 5 runs later -------------------------
echo "Probing the agent before spending a full run..."
PROBE_DIR="$(mktemp -d)"
trap 'rm -rf "$PROBE_DIR"' EXIT
set +e
PROBE_OUT="$(cd "$PROBE_DIR" && codex -a never exec --sandbox workspace-write \
    --json --model "$MODEL" 'Reply with exactly: PROBE_OK' 2>"$PROBE_DIR/err")"
PROBE_RC=$?
set -e

PROBE_TOKENS="$(printf '%s' "$PROBE_OUT" | python - <<'PY'
import json, sys
tot = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        ev = json.loads(line)
    except json.JSONDecodeError:
        continue
    if ev.get("type") == "turn.completed":
        u = ev.get("usage") or {}
        tot += int(u.get("input_tokens", 0) or 0) + int(u.get("output_tokens", 0) or 0)
print(tot)
PY
)"

if [[ $PROBE_RC -ne 0 || "${PROBE_TOKENS:-0}" -eq 0 ]]; then
    echo >&2
    echo "ABORT: the agent is not usable right now (exit=$PROBE_RC, tokens=${PROBE_TOKENS:-0})." >&2
    echo "Codex said:" >&2
    head -20 "$PROBE_DIR/err" | sed 's/^/  /' >&2
    echo >&2
    echo "Quota/429  -> wait for credits, then rerun this script." >&2
    echo "Bad model  -> check '$MODEL' against: codex exec --help" >&2
    echo "Nothing was run and no results were written." >&2
    exit 2
fi
echo "  agent OK (${PROBE_TOKENS} tokens on probe)"
echo

# ------------------------------------------------------------------ baseline
migration-harness batch \
    --dataset "$DATASET" \
    --source Java \
    --target Python \
    --tasks "$TASKS" \
    --experiment baseline \
    --model "$MODEL" \
    --results "$RESULTS" \
    --agent-timeout 1800 \
    --test-timeout 900 \
    --replicates 1

# ------------------------------------------------- postflight: did it work?
echo
echo "Verifying the agent actually did work..."
python - "$RESULTS" "$DATASET" <<'PY'
import json, sys
from pathlib import Path

results, dataset = Path(sys.argv[1]), Path(sys.argv[2])

try:
    null = json.loads((results / "null_baseline.json").read_text())
except FileNotFoundError:
    null = None

def file_count(d: Path, skip=()):
    return sum(1 for p in d.rglob("*")
               if p.is_file() and not any(s in p.parts for s in skip))

rows, bad = [], []
for rp in sorted((results / "baseline").glob("*/result.json")):
    r = json.loads(rp.read_text())
    run = rp.parent
    t, f = r["task"], r["final"]
    turn = r["agent"]["turns"][0]
    usage = r["agent"]["usage"]

    agent_dir = run / "agent"
    wrote = None
    if agent_dir.is_dir():
        pristine = dataset / "target_projects" / t["source"] / t["target"] / t["project"]
        if pristine.is_dir():
            wrote = file_count(agent_dir, skip=(".git", "_source_reference")) - file_count(pristine)

    reasons = []
    if turn["return_code"] != 0:
        reasons.append(f"agent exit {turn['return_code']}")
    if usage["input_tokens"] == 0:
        reasons.append("0 tokens")
    if wrote is not None and wrote <= 0:
        reasons.append("0 new files")
    if r["agent"]["seconds"] < 30:
        reasons.append(f"{r['agent']['seconds']:.0f}s agent time")

    rows.append((t["project"], f, reasons, wrote, r))
    if reasons:
        bad.append(t["project"])

print()
print(f"{'project':<40s} {'tests':>9s} {'raw':>7s} {'norm':>7s}  status")
print("-" * 82)
norms = []
for proj, f, reasons, wrote, r in rows:
    p, tot = f["passed"], f["total"]
    raw = "n/a" if f["pass_rate"] is None else f"{f['pass_rate']:.0%}"
    ns = "n/a"
    if null and proj in null and p is not None and tot:
        nb = null[proj]["null_baseline"]
        np_, nt = nb.get("passed"), nb.get("total")
        if np_ is not None and nt and (tot - np_) > 0:
            v = (p - np_) / (tot - np_)
            norms.append(v)
            ns = f"{v:.0%}"
    status = "INVALID: " + ", ".join(reasons) if reasons else "ok"
    print(f"{proj:<40s} {str(p)+'/'+str(tot):>9s} {raw:>7s} {ns:>7s}  {status}")

print("-" * 82)
valid = [x for x in rows if not x[2]]
print(f"valid runs: {len(valid)}/{len(rows)}")
if norms:
    print(f"mean NORMALISED pass rate: {sum(norms)/len(norms):.1%}")
elif not null:
    print("no null_baseline.json -- run ./run_calibration.sh for normalised scores")
print(f"full success: {sum(1 for x in valid if x[1]['full_success'])}/{len(valid) or 1}")

if bad:
    print()
    print("!! Do not report these numbers. The agent did no work on: " + ", ".join(bad))
    sys.exit(3)
PY

migration-harness summary --results "$RESULTS" --csv "$RESULTS/results.csv"
echo
echo "CSV: $RESULTS/results.csv"
