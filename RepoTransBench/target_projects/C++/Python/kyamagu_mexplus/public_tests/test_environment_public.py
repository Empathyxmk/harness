import pytest

class Environment:
    def __init__(self, code, status):
        self.code = code
        self.status = status

def test_public_environment_emulation():
    env = Environment(42, "system status: critical")

    emulated_write = Environment(env.code, env.status)

    result = Environment(emulated_write.code, emulated_write.status)
    assert result.code == 42
    assert result.status == "system status: critical"

    result.code = -7
    result.status = "shutdown initiated"
    assert result.code == -7
    assert result.status == "shutdown initiated"

    result.status = ""
    assert result.status == ""