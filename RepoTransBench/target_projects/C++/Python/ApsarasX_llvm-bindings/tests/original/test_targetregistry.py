import pytest

# Dummy TargetRegistry for demonstration
class TargetRegistry:
    def __init__(self):
        self.targets = {}

    def register_target(self, name, id_):
        self.targets[name] = id_

    def get_target_id(self, name):
        return self.targets.get(name, -1)

def test_targetregistry_register_and_query():
    reg = TargetRegistry()
    reg.register_target("x86", 1)
    reg.register_target("arm", 2)
    assert reg.get_target_id("x86") == 1
    assert reg.get_target_id("arm") == 2
    assert reg.get_target_id("mips") == -1