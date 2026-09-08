# Primary implementation references

RepoTransBench:
https://github.com/DeepSoftwareAnalytics/RepoTransBench

RepoTransBench's own agent path logic and metadata use:
https://github.com/DeepSoftwareAnalytics/RepoTransBench/blob/main/RepoTransAgent/prompts/system_prompt.py
https://github.com/DeepSoftwareAnalytics/RepoTransBench/blob/main/RepoTransAgent/run.py

Codex CLI:
https://github.com/openai/codex

The harness intentionally uses the public, non-interactive `codex exec --json`
interface and persistent thread IDs for repair turns.
