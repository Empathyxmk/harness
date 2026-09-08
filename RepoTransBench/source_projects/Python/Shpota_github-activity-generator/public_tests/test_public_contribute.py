import os
import sys
import pytest
import shutil
from datetime import datetime, timedelta

# Ensure the project root is in sys.path, so `import contribute` works when running from 'public_tests' or root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import contribute

# Arg class for public tests (copied logic, made public-data args)
class Args:
    def __init__(
        self,
        no_weekends=False,
        max_commits=7,
        frequency=60,
        repository=None,
        user_name=None,
        user_email=None,
        days_before=5,
        days_after=4,
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
    yield
    for d in os.listdir():
        if d.startswith("repository-") and os.path.isdir(d):
            try:
                shutil.rmtree(d)
            except Exception:
                pass

def test_message_and_contributions_per_day_bounds_public(monkeypatch):
    now = datetime.now()
    msg = contribute.message(now)
    # choose different word for check, but still checking part of the message
    assert "Contr" in msg
    # Max commits capped at 20: use a different high value
    args = Args(max_commits=9999)
    monkeypatch.setattr(contribute, "randint", lambda a, b: b)
    assert contribute.contributions_per_day(args) == 20
    # Min commits floored at 1: use a different negative
    args = Args(max_commits=-20)
    assert contribute.contributions_per_day(args) == 1

def test_arguments_and_invalid_args_public(monkeypatch):
    # use different CLI args and values
    out = contribute.arguments([
        '--no_weekends', '--max_commits', '9',
        '--frequency', '10', '--days_after', '6',
        '--repository', 'repo-test', '--user_name', 'Public User',
        '--user_email', 'public-user@example.com'
    ])
    assert out.no_weekends is True
    assert out.max_commits == 9
    assert out.frequency == 10
    assert out.repository == 'repo-test'
    assert out.user_name == 'Public User'
    assert out.user_email == 'public-user@example.com'
    assert out.days_after == 6

    # Invalid arg: use a different malformed flag
    with pytest.raises(SystemExit):
        contribute.arguments(['--notarealarg'])

def test_dates_range_public():
    # use different before/after numbers
    min_day = 10
    max_day = 13
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    days = list(contribute.dates_range(now - timedelta(days=min_day), now + timedelta(days=max_day)))
    assert days[0].date() == (now - timedelta(days=min_day)).date()
    assert days[-1].date() == (now + timedelta(days=max_day)).date()
    assert len(days) == min_day + max_day + 1

def test_is_weekend_public():
    # Check a Sunday and a Tuesday
    sunday = datetime(2023, 7, 9)
    tuesday = datetime(2023, 7, 11)
    assert contribute.is_weekend(sunday)
    assert not contribute.is_weekend(tuesday)