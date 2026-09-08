#!/usr/bin/env bash
# Runs the full experiment ladder and writes a report after every variant.
#   ./run_study.sh                      baseline -> planning -> feedback -> gate
#   ./run_study.sh --variants baseline  just one
#   ./run_study.sh --force              re-run variants that already completed
set -euo pipefail

HARNESS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$HARNESS_DIR"

[[ -f .venv/bin/activate ]] || { echo "ERROR: no .venv here" >&2; exit 1; }
# shellcheck disable=SC1091
source .venv/bin/activate

command -v migration-harness >/dev/null || { echo "ERROR: migration-harness not installed" >&2; exit 1; }
command -v codex >/dev/null || { echo "ERROR: codex not on PATH" >&2; exit 1; }

python "$HARNESS_DIR/study.py" \
    --dataset "$HOME/projects/Harness/RepoTransBench" \
    --tasks   "$HARNESS_DIR/tasks_formal.txt" \
    --results "$HARNESS_DIR/results_formal" \
    --model   "gpt-5.6-terra" \
    --source Java --target Python \
    --agent-timeout 1800 --test-timeout 900 --replicates 1 \
    "$@"
