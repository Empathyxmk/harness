import pytest

# Dummy TargetRegistry for demonstration (public test)
class TargetRegistry:
    def __init__(self):
        self.targets = {}

    def register_target(self, name, id_):
        self.targets[name] = id_

    def get_target_id(self, name):
        return self.targets.get(name, -1)

def test_targetregistry_register_and_query_public():
    reg = TargetRegistry()
    reg.register_target("riscv", 1234)
    reg.register_target("sparc", 5678)
    assert reg.get_target_id("riscv") == 1234
    assert reg.get_target_id("sparc") == 5678
    assert reg.get_target_id("alpha") == -1