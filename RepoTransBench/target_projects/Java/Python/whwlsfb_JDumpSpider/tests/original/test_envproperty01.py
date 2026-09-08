import pytest

class IHeapHolder:
    def findClass(self, var1): raise NotImplementedError
    def getClasses(self): raise NotImplementedError
    def isInstanceOf(self, javaClass, className): raise NotImplementedError
    def isArray(self, javaClass): raise NotImplementedError
    def getSubClasses(self, javaClass): raise NotImplementedError
    def getInstances(self, javaClass): raise NotImplementedError
    def getFields(self, javaClass): raise NotImplementedError
    def getClassName(self, javaClass): raise NotImplementedError
    def getSuperClass(self, javaClass): raise NotImplementedError
    def getFieldName(self, field): raise NotImplementedError
    def getFieldClass(self, field): raise NotImplementedError
    def findThing(self, objectId): raise NotImplementedError
    def getValueOfField(self, instance, fieldName): raise NotImplementedError
    def getFieldsByNameList(self, instance, fieldList): raise NotImplementedError
    def arrayDump(self, instance): raise NotImplementedError
    def getArrayItems(self, instance): raise NotImplementedError
    def getFieldStringValue(self, instance, fieldName): raise NotImplementedError
    def getFieldValue(self, instance, fieldName): raise NotImplementedError
    def isMap(self, instance): raise NotImplementedError
    def getMap(self, instance): raise NotImplementedError
    def toString(self, instance): raise NotImplementedError
    def toByteArray(self, _instance): raise NotImplementedError

class EnvProperty01:
    def getName(self):
        return "ProcessEnvironment"

    def sniff(self, heapHolder):
        try:
            found_cls = heapHolder.findClass("java.lang.ProcessEnvironment")
            if not found_cls:
                return None
            instances = heapHolder.getInstances(found_cls)
            # Just grab the first result from arrayDump
            for instance in instances:
                envmap = heapHolder.arrayDump(instance)
                for k, v in envmap.items():
                    return f"{k}={v}"
        except Exception:
            # as per Java: should not raise
            pass
        return None

class DummyHeapHolder(IHeapHolder):
    def findClass(self, var1):
        return self if var1 == "java.lang.ProcessEnvironment" else None
    def getClasses(self): return None
    def isInstanceOf(self, javaClass, className): return False
    def isArray(self, javaClass): return False
    def getSubClasses(self, javaClass): return []
    def getInstances(self, javaClass): return [object()]
    def getFields(self, javaClass): return []
    def getClassName(self, javaClass): return None
    def getSuperClass(self, javaClass): return None
    def getFieldName(self, field): return None
    def getFieldClass(self, field): return None
    def findThing(self, objectId): return None
    def getValueOfField(self, instance, fieldName): return None
    def getFieldsByNameList(self, instance, fieldList): return {}
    def arrayDump(self, instance): return {"ENVVAR": "VAL"}
    def getArrayItems(self, instance): return []
    def getFieldStringValue(self, instance, fieldName): return None
    def getFieldValue(self, instance, fieldName): return None
    def isMap(self, instance): return isinstance(instance, dict)
    def getMap(self, instance): return object()
    def toString(self, instance): return None
    def toByteArray(self, _instance): return b''

def test_get_name():
    env = EnvProperty01()
    assert env.getName() == "ProcessEnvironment"

def test_sniff_happy_path():
    env = EnvProperty01()
    heapHolder = DummyHeapHolder()
    s = env.sniff(heapHolder)
    assert "ENVVAR" in s
    assert "VAL" in s

def test_sniff_handles_exception():
    env = EnvProperty01()
    class ExHeapHolder(DummyHeapHolder):
        def getMap(self, instance): raise RuntimeError("bad")
    heapHolder = ExHeapHolder()
    # Should not throw
    env.sniff(heapHolder)

def test_sniff_no_class_found():
    env = EnvProperty01()
    class Dummy(DummyHeapHolder):
        def findClass(self, var1): return None
    heapHolder = Dummy()
    assert env.sniff(heapHolder) is None