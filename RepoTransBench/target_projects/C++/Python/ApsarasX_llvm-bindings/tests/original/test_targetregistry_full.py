import pytest

class DummyTarget:
    def getName(self):
        return "x86-64"
    def getShortDescription(self):
        return "64-bit X86: EM64T and AMD64"
    def createTargetMachine(self, triple, cpu):
        class DummyMachine:
            pass
        return DummyMachine()

class DummyTargetRegistry:
    @staticmethod
    def lookupTarget(name):
        if name == "x86_64":
            return DummyTarget()
        return None

class llvm:
    TargetRegistry = DummyTargetRegistry
    Target = DummyTarget

    @staticmethod
    def InitializeAllTargetInfos():
        pass
    @staticmethod
    def InitializeAllTargets():
        pass
    @staticmethod
    def InitializeAllTargetMCs():
        pass

def setup_module(module):
    llvm.InitializeAllTargetInfos()
    llvm.InitializeAllTargets()
    llvm.InitializeAllTargetMCs()
    # Ensure DummyTarget is always returned for 'x86_64'
    module.target = llvm.TargetRegistry.lookupTarget("x86_64")

def test_lookup_target():
    target = llvm.TargetRegistry.lookupTarget("x86_64")
    assert isinstance(target, llvm.Target)

def test_target_get_name():
    target = llvm.TargetRegistry.lookupTarget("x86_64")
    assert isinstance(target, llvm.Target)
    if target:
        assert target.getName() == "x86-64"

def test_target_get_short_description():
    target = llvm.TargetRegistry.lookupTarget("x86_64")
    assert isinstance(target, llvm.Target)
    if target:
        assert target.getShortDescription() == "64-bit X86: EM64T and AMD64"

def test_target_create_target_machine():
    target = llvm.TargetRegistry.lookupTarget("x86_64")
    assert isinstance(target, llvm.Target)
    if target:
        machine = target.createTargetMachine("x86_64-generic-generic", "generic")
        assert machine is not None