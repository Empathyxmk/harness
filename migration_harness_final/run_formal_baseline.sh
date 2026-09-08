#!/usr/bin/env bash
set -euo pipefail

HARNESS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATASET="$HOME/projects/Harness/RepoTransBench"
TASKS="$HARNESS_DIR/tasks_formal.txt"
RESULTS="$HARNESS_DIR/results_formal"
MODEL="gpt-5.6-terra"

cd "$HARNESS_DIR"

[[ -f .venv/bin/activate ]] || { echo "ERROR: no .venv here" >&2; exit 1; }
source .venv/bin/activate
[[ -f "$TASKS" ]] || { echo "ERROR: missing $TASKS" >&2; exit 1; }
[[ -d "$DATASET/source_projects" && -d "$DATASET/target_projects" ]] || { echo "ERROR: bad dataset $DATASET" >&2; exit 1; }
command -v migration-harness >/dev/null || { echo "ERROR: migration-harness not installed" >&2; exit 1; }
command -v codex >/dev/null || { echo "ERROR: codex not on PATH" >&2; exit 1; }

# --- archive previous (invalid) baseline runs so they can't pollute summary --
if [[ -d "$RESULTS/baseline" ]] && compgen -G "$RESULTS/baseline/*/result.json" >/dev/null; then
    ARCHIVE="$HARNESS_DIR/results_formal_archived_$(date -u +%Y%m%dT%H%M%SZ)"
    mkdir -p "$ARCHIVE"
    mv "$RESULTS/baseline" "$ARCHIVE/baseline"
    rm -f "$RESULTS/results.csv"
    echo "Archived previous baseline runs -> $ARCHIVE"
    echo
fi

echo "Formal baseline"
echo "  model   : $MODEL"
echo "  codex   : $(codex --version 2>&1 | head -1)"
echo "  dataset : $DATASET"
echo "  results : $RESULTS"
echo
echo "Projects:"
sed '/^[[:space:]]*$/d; /^[[:space:]]*#/d' "$TASKS" | sed 's/^/  /'
echo

# --- probe Codex under the same conditions the real runs use (a git repo) ---
echo "Checking Codex is usable..."
PROBE="$(mktemp -d)"
trap 'rm -rf "$PROBE"' EXIT
git -C "$PROBE" init -q
set +e
PROBE_OUT="$(cd "$PROBE" && codex -a never exec --sandbox workspace-write \
    --json --model "$MODEL" 'Reply with exactly: PROBE_OK' 2>"$PROBE/err")"
PROBE_RC=$?
set -e

if [[ $PROBE_RC -ne 0 ]] || ! grep -q 'turn.completed' <<<"$PROBE_OUT"; then
    echo >&2
    echo "ABORT: Codex could not run (exit $PROBE_RC). Nothing was executed." >&2
    echo "Codex said:" >&2
    head -20 "$PROBE/err" | sed 's/^/  /' >&2
    echo >&2
    echo "If this mentions quota, rate limit or 429, wait for credits and rerun." >&2
    exit 2
fi
echo "  Codex OK"
echo

# ------------------------------------------------------------------ run it --
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

echo
migration-harness summary --results "$RESULTS" --csv "$RESULTS/results.csv"

# --------------------------------------------------------------- per-task ---
echo
python - "$RESULTS" <<'PY'
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
bad = []
for p in sorted(root.glob("baseline/*/result.json")):
    r = json.loads(p.read_text())
    f, a = r["final"], r["agent"]
    rc = a["turns"][0]["return_code"]
    tok = a["usage"]["input_tokens"]
    rate = "n/a" if f["pass_rate"] is None else f"{f['pass_rate']:.1%}"
    print(f"\n{r['task']['project']}")
    print(f"  agent exit   : {rc}")
    print(f"  agent time   : {a['seconds']:.1f}s")
    print(f"  input tokens : {tok}")
    print(f"  tests        : {f['passed']}/{f['total']}  ({rate})")
    print(f"  full success : {f['full_success']}")
    if rc != 0 or tok == 0 or a["seconds"] < 30:
        bad.append(r["task"]["project"])
if bad:
    print("\n" + "!" * 70)
    print("WARNING: the agent did no real work on: " + ", ".join(bad))
    print("Those rows are not valid results. Do not report them.")
    print("!" * 70)
PY

echo
echo "CSV: $RESULTS/results.csv"
