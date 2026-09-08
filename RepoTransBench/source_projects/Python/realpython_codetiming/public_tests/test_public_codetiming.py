import math
import re
import time

import pytest

from codetiming import Timer, TimerError

USER_TIME_PREFIX = "Time spent:"
USER_TIME_MESSAGE = f"{USER_TIME_PREFIX} {{:.5f}} s"
RE_USER_TIME_MESSAGE = re.compile(USER_TIME_PREFIX + r" 0\.\d{5} s")
RE_USER_TIME_MESSAGE_INITIAL_TEXT_TRUE = re.compile(
    f"Timer launched\n{USER_TIME_PREFIX}" + r" 0\.\d{5} s"
)
RE_USER_TIME_MESSAGE_INITIAL_TEXT_CUSTOM = re.compile(
    f"Begin timer!\n{USER_TIME_PREFIX}" + r" 0\.\d{5} s"
)

def waste_custom_time(num: int = 500) -> None:
    sum(n+1 for n in range(num))

@Timer(text=USER_TIME_MESSAGE)
def decorated_time_public(num: int = 500) -> None:
    sum(n+1 for n in range(num))

@Timer(text=USER_TIME_MESSAGE, initial_text=True)
def decorated_time_initial_true_public(num: int = 500) -> None:
    sum(n+1 for n in range(num))

@Timer(text=USER_TIME_MESSAGE, initial_text="Begin timer!")
def decorated_time_initial_custom_public(num: int = 500) -> None:
    sum(n+1 for n in range(num))

@Timer(name="bucket", text=USER_TIME_MESSAGE)
def accumulated_time_public(num: int = 500) -> None:
    sum(n+1 for n in range(num))

class MyLogger:
    def __init__(self):
        self.logs = ""
    def __call__(self, msg: str):
        self.logs += msg

def test_timer_as_decorator_public(capsys: pytest.CaptureFixture[str]) -> None:
    decorated_time_public()
    stdout, stderr = capsys.readouterr()
    assert RE_USER_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""

def test_timer_as_context_manager_public(capsys: pytest.CaptureFixture[str]) -> None:
    with Timer(text=USER_TIME_MESSAGE):
        waste_custom_time()
    stdout, stderr = capsys.readouterr()
    assert RE_USER_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""

def test_explicit_timer_public(capsys: pytest.CaptureFixture[str]) -> None:
    t = Timer(text=USER_TIME_MESSAGE)
    t.start()
    waste_custom_time()
    t.stop()
    stdout, stderr = capsys.readouterr()
    assert RE_USER_TIME_MESSAGE.match(stdout)
    assert stdout.count("\n") == 1
    assert stderr == ""

def test_error_if_timer_not_running_public() -> None:
    t = Timer(text=USER_TIME_MESSAGE)
    with pytest.raises(TimerError):
        t.stop()

def test_access_timer_object_in_context_public(capsys: pytest.CaptureFixture[str]) -> None:
    with Timer(text=USER_TIME_MESSAGE) as t:
        assert isinstance(t, Timer)
        assert isinstance(t.text, str)
        assert t.text.startswith(USER_TIME_PREFIX)
    _, _ = capsys.readouterr()

def test_custom_logger_public():
    logger = MyLogger()
    with Timer(text=USER_TIME_MESSAGE, logger=logger):
        waste_custom_time()
    assert RE_USER_TIME_MESSAGE.match(logger.logs)

def test_timer_without_text_public(capsys: pytest.CaptureFixture[str]) -> None:
    with Timer(logger=None):
        waste_custom_time()
    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""

def test_accumulated_decorator_public(capsys: pytest.CaptureFixture[str]) -> None:
    accumulated_time_public()
    accumulated_time_public()
    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_USER_TIME_MESSAGE.match(lines[0])
    assert RE_USER_TIME_MESSAGE.match(lines[1])
    assert stderr == ""

def test_accumulated_context_manager_public(capsys: pytest.CaptureFixture[str]) -> None:
    t = Timer(name="bucket", text=USER_TIME_MESSAGE)
    with t:
        waste_custom_time()
    with t:
        waste_custom_time()
    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_USER_TIME_MESSAGE.match(lines[0])
    assert RE_USER_TIME_MESSAGE.match(lines[1])
    assert stderr == ""

def test_accumulated_explicit_timer_public(capsys: pytest.CaptureFixture[str]) -> None:
    t = Timer(name="explicit_bucket", text=USER_TIME_MESSAGE)
    total = 0.0
    t.start()
    waste_custom_time()
    total += t.stop()
    t.start()
    waste_custom_time()
    total += t.stop()
    stdout, stderr = capsys.readouterr()
    lines = stdout.strip().split("\n")
    assert len(lines) == 2
    assert RE_USER_TIME_MESSAGE.match(lines[0])
    assert RE_USER_TIME_MESSAGE.match(lines[1])
    assert stderr == ""
    assert total == Timer.timers["explicit_bucket"]

def test_error_if_restarting_running_timer_public() -> None:
    t = Timer(text=USER_TIME_MESSAGE)
    t.start()
    with pytest.raises(TimerError):
        t.start()

def test_last_starts_as_nan_public() -> None:
    t = Timer()
    assert math.isnan(t.last)

def test_timer_sets_last_public() -> None:
    with Timer(logger=None) as t:
        time.sleep(0.01)
    assert t.last >= 0.01