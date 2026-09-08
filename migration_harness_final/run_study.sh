#!/usr/bin/env bash
# Runs the experiment ladder and writes a report after every variant.
#
#   ./run_study.sh --variants baseline                       one variant
#   ./run_study.sh --variants baseline,planning              resumes, adds planning
#   ./run_study.sh                                           all four
#   ./run_study.sh --report-only                             regenerate reports
#
# Resumes at (experiment, project, replicate) granularity, so an interrupted
# variant is completed rather than re-run. Calibration is run automatically if
# results_formal/null_baseline.json is missing (needs no agent credits).
set -euo pipefail

HARNESS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DATASET="$HOME/projects/Harness/RepoTransBench"
TASKS="$HARNESS_DIR/tasks_formal.txt"
RESULTS="$HARNESS_DIR/results_formal"
MODEL="gpt-5.6-terra"

cd "$HARNESS_DIR"

[[ -f .venv/bin/activate ]] || { echo "ERROR: no .venv in $HARNESS_DIR" >&2; exit 1; }
# shellcheck disable=SC1091
source .venv/bin/activate

[[ -f "$TASKS" ]] || { echo "ERROR: missing $TASKS" >&2; exit 1; }
[[ -f study.py ]] || { echo "ERROR: study.py not found in $HARNESS_DIR" >&2; exit 1; }
command -v migration-harness >/dev/null || { echo "ERROR: migration-harness not installed" >&2; exit 1; }
command -v codex >/dev/null || { echo "ERROR: codex not on PATH" >&2; exit 1; }

# --- calibration is a precondition, and costs no credits --------------------
if [[ ! -f "$RESULTS/null_baseline.json" ]]; then
    echo "No null_baseline.json found. Calibrating the task set first"
    echo "(scores the untouched scaffold; no agent credits used)."
    echo
    migration-harness calibrate \
        --dataset "$DATASET" \
        --source Java --target Python \
        --tasks "$TASKS" \
        --results "$RESULTS"
    echo
fi

python "$HARNESS_DIR/study.py" \
    --dataset "$DATASET" \
    --tasks   "$TASKS" \
    --results "$RESULTS" \
    --model   "$MODEL" \
    --source Java --target Python \
    --agent-timeout 1800 --test-timeout 900 --replicates 1 \
    "$@"
