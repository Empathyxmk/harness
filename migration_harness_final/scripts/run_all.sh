#!/usr/bin/env bash
set -euo pipefail

DATASET="${1:?usage: run_all.sh DATASET TASKS_FILE [REPLICATES]}"
TASKS="${2:?usage: run_all.sh DATASET TASKS_FILE [REPLICATES]}"
REPS="${3:-1}"

for EXP in baseline planning feedback gate; do
  migration-harness batch \
    --dataset "$DATASET" \
    --source Java \
    --target Python \
    --tasks "$TASKS" \
    --experiment "$EXP" \
    --replicates "$REPS"
done

migration-harness summary --results results --csv results/results.csv
