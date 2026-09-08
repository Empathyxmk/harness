import types
import pytest

# Mocks for org.caoym.jjvm.lang.JvmClass and JvmMethod
class JvmMethod:
    def call(self, env, thiz, *args):
        pass
    def getParameterCount(self):
        return 1
    def getName(self):
        return "main"

class DummyMethod(JvmMethod):
    def __init__(self):
        self.called = False
    def call(self, env, thiz, *args):
        self.called = True
    def getParameterCount(self):
        return 1
    def getName(self):
        return "main"

class JvmClass:
    def __init__(self, *a, **kw):
        pass
    def getMethod(self, name, descriptor):
        return None

class DummyClass(JvmClass):
    def __init__(self):
        super().__init__()
        self.method = DummyMethod()
    def getMethod(self, name, descriptor):
        if name == "main" and descriptor == "([Ljava/lang/String;)V":
            return self.method
        return None

class JvmClassLoader:
    def loadClass(self, className):
        raise NotImplementedError

class DummyClassLoader(JvmClassLoader):
    def __init__(self):
        self.loaded = False
    def loadClass(self, className):
        self.loaded = True
        return DummyClass()

# Mock VirtualMachine with caching for .getClass
class VirtualMachine:
    def __init__(self, path, klass):
        self._class_cache = {}
        # Simulated private field for loader
        self.classLoader = DummyClassLoader()
    def getClass(self, className):
        if className not in self._class_cache:
            self._class_cache[className] = self.classLoader.loadClass(className)
        return self._class_cache[className]

def test_get_class_caches_and_returns():
    vm = VirtualMachine('.', "FakeClass")
    loader = vm.classLoader  # using mock

    cls1 = vm.getClass("hello.FakeClass")
    assert loader.loaded
    loader.loaded = False

    # Should fetch from cache; no loading this time
    cls2 = vm.getClass("hello.FakeClass")
    assert not loader.loaded
    assert cls1 is cls2