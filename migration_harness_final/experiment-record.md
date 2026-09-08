# Experiment Record

## Fixed setup

- Migration: Java to Python
- Model: gpt-5.6-terra
- Reasoning effort: medium
- Codex CLI: 0.153.4
- Agent timeout: 1800 seconds
- Test timeout: 900 seconds
- Replicates: 1
- Projects:
  - c0ny1_chunked-coding-converter
  - binarywang_java-emoji-converter
  - LatencyUtils_LatencyUtils

## Baseline

The baseline performs one Codex migration pass with general instructions.

Results:

| Project | Passed | Total | Pass rate | Full success |
|---|---:|---:|---:|---:|
| c0ny1_chunked-coding-converter | 40 | 40 | 100% | Yes |
| binarywang_java-emoji-converter | 19 | 19 | 100% | Yes |
| LatencyUtils_LatencyUtils | 17 | 20 | 85% | No |

Overall migration success: 2/3 (66.7%).
Mean project test pass rate: 95.0%.

### Failure analysis

LatencyUtils failed three tests concerning moving-window arithmetic and pause
handling. Two failures were visible in the public suite. The results suggest
that the agent implemented the broad interface successfully but did not fully
reconstruct the original algorithms and edge-case state transitions.

### Iteration 1 hypothesis

Mandatory repository analysis and component-level planning may improve fidelity
for stateful algorithms while preserving performance on the two already
successful projects.
