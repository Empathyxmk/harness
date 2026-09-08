# Migration Harness

A deliberately small experimental harness for repository-level code migration.

It combines:

- **RepoTransBench** — benchmark and executable tests
- **Codex CLI** — coding agent
- **this harness** — isolation, iteration, evaluation, metrics

## Commands

```bash
pip install -e .

migration-harness experiments

migration-harness list \
  --dataset /path/to/repotransbench-data \
  --source Java \
  --target Python

migration-harness run \
  --dataset /path/to/repotransbench-data \
  --source Java \
  --target Python \
  --project PROJECT_NAME \
  --experiment baseline
```

Experiments:

- `baseline` — one Codex pass
- `planning` — baseline + mandatory repository analysis/plan
- `feedback` — planning + one public-test repair round
- `gate` — planning + deterministic public-test gate, up to 3 repairs

Batch file (`tasks.txt`):

```text
project_a
project_b
project_c
```

Then:

```bash
migration-harness batch \
  --dataset /path/to/data \
  --tasks tasks.txt \
  --experiment baseline

migration-harness summary \
  --results results \
  --csv results/results.csv
```

## Evaluation integrity

The agent gets the complete source repository plus public tests, but
`target_original_tests` are removed from its workspace.

For public feedback, the harness copies the agent output to a separate
evaluation directory, restores pristine public tests and `run_tests.sh`, keeps
held-out tests absent, then runs the benchmark runner.

For final evaluation, it again copies the agent output, restores pristine
public tests, held-out/original tests, and `run_tests.sh`, then runs the
benchmark runner.

Therefore agent edits to tests or the test runner never affect the score, and
hidden-test failures are never fed back to the agent.

## Platform

Use Linux/macOS, or WSL2 on Windows. RepoTransBench uses Bash test runners.
The harness requires:

- Python 3.10+
- Git
- Bash
- authenticated `codex` CLI on PATH
