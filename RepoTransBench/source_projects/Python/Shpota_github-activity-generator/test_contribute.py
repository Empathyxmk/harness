import os
import sys
import types
import pytest
import shutil
from datetime import datetime, timedelta

import contribute

# Helper Arg class to simulate argparse.Namespace
class Args:
    def __init__(
        self,
        no_weekends=False,
        max_commits=10,
        frequency=80,
        repository=None,
        user_name=None,
        user_email=None,
        days_before=2,
        days_after=2,
    ):
        self.no_weekends = no_weekends
        self.max_commits = max_commits
        self.frequency = frequency
        self.repository = repository
        self.user_name = user_name
        self.user_email = user_email
        self.days_before = days_before
        self.days_after = days_after

@pytest.fixture(autouse=True)
def cleanup_repos():
    # Clean up before and after each test
    yield
    for d in os.listdir():
        if d.startswith("repository-") and os.path.isdir(d):
            try:
                shutil.rmtree(d)
            except Exception:
                pass

def test_message_and_contributions_per_day_bounds(monkeypatch):
    # Test message formatting and contributions_per_day capping
    now = datetime.now()
    msg = contribute.message(now)
    assert "Contribution" in msg
    # Max commits capped at 20
    args = Args(max_commits=50)
    monkeypatch.setattr(contribute, "randint", lambda a, b: b)
    assert contribute.contributions_per_day(args) == 20
    # Min commits floored at 1
    args = Args(max_commits=-5)
    assert contribute.contributions_per_day(args) == 1

def test_arguments_and_invalid_args(monkeypatch):
    # Test parsing of CLI arguments
    out = contribute.arguments([
        '--no_weekends', '--max_commits', '4',
        '--frequency', '50', '--days_before', '3',
        '--days_after', '1'
    ])
    assert out.no_weekends is True
    assert out.max_commits == 4
    assert out.frequency == 50
    assert out.days_before == 3
    assert out.days_after == 1

def test_main_negative_days(monkeypatch):
    # main should sys.exit if days_before or days_after are negative
    monkeypatch.setattr(sys, "exit", lambda msg: (_ for _ in ()).throw(SystemExit(msg)))
    with pytest.raises(SystemExit) as e:
        contribute.main([
            "--days_before", "-2"
        ])
    assert "must not be negative" in str(e.value)
    with pytest.raises(SystemExit) as e:
        contribute.main([
            "--days_after", "-2"
        ])
    assert "must not be negative" in str(e.value)

def test_run_and_contribute(monkeypatch, tmp_path):
    # Test contribute(), run(), and README.md writing logic
    called = []
    monkeypatch.setattr(contribute, "run", lambda c: called.append(list(c)))
    test_dir = tmp_path / "foo"
    test_dir.mkdir()
    monkeypatch.setattr(os, "getcwd", lambda: str(test_dir))
    dt = datetime(2023, 2, 17, 15, 45)
    contribute.contribute(dt)
    f = test_dir / "README.md"
    assert f.exists()
    content = f.read_text()
    assert "Contribution:" in content
    # run() with a process that always returns 0
    import subprocess
    monkeypatch.setattr(subprocess, "Popen", lambda c: types.SimpleNamespace(wait=lambda : 0))
    contribute.run(["ls"])

def test_main_minimal(monkeypatch, tmp_path):
    # Simulate a minimal main run with no repository/user_name/email, few days, and predictable random

    # Patch os.mkdir to a dummy that only prevents actual file system change
    orig_os_mkdir = os.mkdir
    def fake_mkdir(path, mode=0o777):
        # simulate directory creation but don't really change fs
        return None
    monkeypatch.setattr(os, "mkdir", fake_mkdir)
    monkeypatch.setattr(os, "chdir", lambda d: None)
    monkeypatch.setattr(contribute, "run", lambda c: None)
    monkeypatch.setattr(contribute, "contribute", lambda d: None)
    now = datetime(2023, 2, 21, 13, 0)
    monkeypatch.setattr(contribute, "datetime", types.SimpleNamespace(
        now=lambda: now, timedelta=timedelta))
    monkeypatch.setattr(contribute, "randint", lambda a, b: 0)
    args = [
        "--days_before", "1", "--days_after", "1", "--max_commits", "1"
    ]
    contribute.main(args)

def test_main_with_repository(monkeypatch, tmp_path):
    # Simulate a main run with repository/user_name/email

    # Patch os.mkdir to a dummy that only prevents actual file system change
    def fake_mkdir(path, mode=0o777):
        # simulate directory creation but don't really change fs
        return None
    monkeypatch.setattr(os, "mkdir", fake_mkdir)
    monkeypatch.setattr(os, "chdir", lambda d: None)
    calls = []
    monkeypatch.setattr(contribute, "run", lambda c: calls.append(c))
    monkeypatch.setattr(contribute, "contribute", lambda d: None)
    now = datetime(2023, 2, 21, 13, 0)
    monkeypatch.setattr(contribute, "datetime", types.SimpleNamespace(
        now=lambda: now, timedelta=timedelta))
    monkeypatch.setattr(contribute, "randint", lambda a, b: 100)  # pass frequency
    args = [
        "--repository", "https://github.com/testuser/somerepo.git",
        "--user_name", "foo", "--user_email", "bar@test.com",
        "--days_before", "1", "--days_after", "1"
    ]
    contribute.main(args)
    # Ensure the git remote and push commands were called
    git_calls = [c for c in calls if "git" in c]
    assert any("remote" in c for c in git_calls)
    assert any("push" in c for c in git_calls)