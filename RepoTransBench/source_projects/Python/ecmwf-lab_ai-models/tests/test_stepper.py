import time
import logging

import src.ai_models.stepper as stepper

def test_stepper_basic(monkeypatch, caplog):
    s = stepper.Stepper(step=2, lead_time=6)
    assert s.num_steps == 3
    with s:
        s(0, 2)
        s(1, 2)
        s(2, 2)
    # Check elapsed log output
    logs = caplog.text
    assert "Elapsed" in logs
    assert "Average" in logs

def test_stepper_zero_steps(caplog):
    s = stepper.Stepper(step=5, lead_time=0)
    with s:
        pass  # Should not log Average per step