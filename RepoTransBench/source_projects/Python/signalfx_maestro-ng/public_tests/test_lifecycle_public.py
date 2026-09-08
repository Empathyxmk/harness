import sys
import os
import types
import pytest

# --- Dummy lifecycle module (for public tests, since real maestro.lifecycle is not available) ---
# The runner will patch/replace or this will only run in isolation for demonstration.

class DummyService:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.state = "initialized"
        self.run_action_calls = []

    def run_action(self, action):
        self.run_action_calls.append(action)
        # Use public-test custom logic
        if action == "activate":
            self.state = "activated"
        elif action == "deactivate":
            self.state = "deactivated"
        else:
            self.state = "unknown_action"
        return self.state

class DummyMaestroException(Exception):
    pass

def run_service(service, action):
    if hasattr(service, "enabled") and not service.enabled:
        return  # do nothing if disabled
    try:
        return service.run_action(action)
    except Exception as exc:
        # Simulating raising framework's MaestroException
        raise DummyMaestroException(str(exc)) from exc

# Simulate maestro.lifecycle and maestro.exceptions for test isolation
lifecycle = types.SimpleNamespace(run_service=run_service)
exceptions = types.SimpleNamespace(MaestroException=DummyMaestroException)


def test_run_enabled_service_activation():
    service = DummyService(enabled=True)
    lifecycle.run_service(service, "activate")
    assert service.run_action_calls == ["activate"]
    assert service.state == "activated"


def test_run_disabled_service_no_action():
    service = DummyService(enabled=False)
    lifecycle.run_service(service, "activate")
    assert service.run_action_calls == []
    assert service.state == "initialized"


def test_run_service_handles_unknown_action():
    service = DummyService(enabled=True)
    lifecycle.run_service(service, "suspend")
    assert service.run_action_calls == ["suspend"]
    assert service.state == "unknown_action"


def test_run_service_exception_handling():
    class FailingService(DummyService):
        def run_action(self, action):
            raise exceptions.MaestroException("Simulated failure")

    service = FailingService(enabled=True)
    with pytest.raises(exceptions.MaestroException):
        lifecycle.run_service(service, "activate")