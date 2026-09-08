# Mocks for org.caoym.jjvm.lang.JvmField, JvmMethod
import pytest

class Env:
    pass

class JvmField:
    # Simulate dynamic instance variables if needed
    def set(self, env, thiz, value):
        raise NotImplementedError()
    def get(self, env, thiz):
        raise NotImplementedError()

class JvmMethod:
    def call(self, env, thiz, *args):
        raise NotImplementedError()
    def getParameterCount(self):
        raise NotImplementedError()
    def getName(self):
        raise NotImplementedError()

def test_jvm_field():
    class MyField(JvmField):
        def __init__(self):
            self.v = None
        def set(self, env, thiz, value):
            self.v = value
        def get(self, env, thiz):
            return self.v
    field = MyField()
    field.set(None, None, "abc")
    assert field.get(None, None) == "abc"

def test_jvm_method():
    class MyMethod(JvmMethod):
        def __init__(self):
            self.called = False
        def call(self, env, thiz, *args):
            self.called = True
        def getParameterCount(self):
            return 1
        def getName(self):
            return "hello"
    method = MyMethod()
    method.call(None, None)
    assert method.getParameterCount() == 1
    assert method.getName() == "hello"