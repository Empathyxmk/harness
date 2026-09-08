# Mirroring the likely pattern of JvmFieldMethodTest with different properties
import pytest

class JvmField:
    def __init__(self, name, descriptor, owner=None, is_static=False, is_final=False, is_volatile=False):
        self._name = name
        self._descriptor = descriptor
        self._owner = owner
        self._is_static = is_static
        self._is_final = is_final
        self._is_volatile = is_volatile
    def getName(self):
        return self._name
    def getDescriptor(self):
        return self._descriptor
    def isStatic(self):
        return self._is_static
    def isFinal(self):
        return self._is_final
    def isVolatile(self):
        return self._is_volatile

class JvmMethod:
    def call(self, env, thiz, *args):
        pass
    def getParameterCount(self):
        return 8
    def getName(self):
        return "doPublicStuff"

class AltPublicField(JvmField):
    def __init__(self):
        super().__init__("publicField99", "D", None, True, False, True)

class AltPublicMethod(JvmMethod):
    def call(self, env, thiz, *args):
        pass
    def getParameterCount(self):
        return 8
    def getName(self):
        return "doPublicStuff"

def test_create_alt_public_field_and_method():
    field = AltPublicField()
    method = AltPublicMethod()
    assert field.getName() == "publicField99"
    assert field.getDescriptor() == "D"
    assert field.isStatic()
    assert not field.isFinal()
    assert field.isVolatile()
    assert method.getName() == "doPublicStuff"
    assert method.getParameterCount() == 8