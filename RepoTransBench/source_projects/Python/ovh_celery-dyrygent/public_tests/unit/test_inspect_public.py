import pytest
from celery_dyrygent.celery import inspect

def test_queue_length_returns_int_type(monkeypatch):
    # Use an alternate mocked return value and queue name
    monkeypatch.setattr(inspect, "inspect_command", lambda *_, **__: {"other-queue": 5})
    result = inspect.queue_length("other-queue")
    assert isinstance(result, int)
    assert result == 5

def test_queue_length_returns_zero_for_missing_queue(monkeypatch):
    # Provide a mapping where the tested queue is NOT found
    monkeypatch.setattr(inspect, "inspect_command", lambda *_, **__: {"sample-queue": 3})
    # Queue name that is not in mapping
    result = inspect.queue_length("unseen-queue")
    assert result == 0

def test_inspect_command_handles_empty(monkeypatch):
    monkeypatch.setattr(inspect, "inspect_command", lambda *_, **__: {})
    assert inspect.queue_length("noqueue") == 0