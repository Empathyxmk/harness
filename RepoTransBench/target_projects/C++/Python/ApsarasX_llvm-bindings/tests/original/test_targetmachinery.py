import pytest

class DummyDataLayout:
    pass

class DummyTargetMachine:
    def create_data_layout(self):
        return DummyDataLayout()

class DummyTarget:
    def create_target_machine(self, triple, cpu):
        return DummyTargetMachine()

class DummyTargetRegistry:
    @staticmethod
    def lookup_target(name):
        if name == "x86_64":
            return DummyTarget()
        return None

class llvm:
    TargetRegistry = DummyTargetRegistry
    Target = DummyTarget
    TargetMachine = DummyTargetMachine
    DataLayout = DummyDataLayout

    @staticmethod
    def InitializeAllTargetInfos():
        pass
    @staticmethod
    def InitializeAllTargets():
        pass
    @staticmethod
    def InitializeAllTargetMCs():
        pass

def test_targetmachine_create_datalayout():
    llvm.InitializeAllTargetInfos()
    llvm.InitializeAllTargets()
    llvm.InitializeAllTargetMCs()
    target = llvm.TargetRegistry.lookup_target('x86_64')
    assert isinstance(target, llvm.Target)
    if target:
        machine = target.create_target_machine('x86_64-unknown-unknown', 'generic')
        data_layout = machine.create_data_layout()
        assert isinstance(data_layout, llvm.DataLayout)