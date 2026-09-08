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
            found_cls = heapHolder.findClass("java.lang.PublicProcessEnvironment")
            if not found_cls:
                return None
            instances = heapHolder.getInstances(found_cls)
            for instance in instances:
                envmap = heapHolder.arrayDump(instance)
                for k, v in envmap.items():
                    return f"{k}={v}"
        except Exception:
            pass
        return None

class PublicDummyHeapHolder(IHeapHolder):
    def findClass(self, var1):
        return self if var1 == "java.lang.PublicProcessEnvironment" else None
    def getClasses(self): return None
    def isInstanceOf(self, javaClass, className): return False
    def isArray(self, javaClass): return False
    def getSubClasses(self, javaClass): return []
    def getInstances(self, javaClass): return [object(), object()]
    def getFields(self, javaClass): return []
    def getClassName(self, javaClass): return None
    def getSuperClass(self, javaClass): return None
    def getFieldName(self, field): return None
    def getFieldClass(self, field): return None
    def findThing(self, objectId): return None
    def getValueOfField(self, instance, fieldName): return None
    def getFieldsByNameList(self, instance, fieldList): return {}
    def arrayDump(self, instance): return {"PUBLIC_ENV": "VALUE42"}
    def getArrayItems(self, instance): return []
    def getFieldStringValue(self, instance, fieldName): return None
    def getFieldValue(self, instance, fieldName): return None
    def isMap(self, instance): return isinstance(instance, dict)
    def getMap(self, instance): return {}
    def toString(self, instance): return None
    def toByteArray(self, _instance): return b''

def test_get_name_public():
    env = EnvProperty01()
    assert env.getName() == "ProcessEnvironment"

def test_sniff_happy_path_public():
    env = EnvProperty01()
    heapHolder = PublicDummyHeapHolder()
    s = env.sniff(heapHolder)
    assert "PUBLIC_ENV" in s
    assert "VALUE42" in s

def test_sniff_handles_exception_public():
    env = EnvProperty01()
    class ExHeapHolder(PublicDummyHeapHolder):
        def getMap(self, instance): raise RuntimeError("bad_public")
    heapHolder = ExHeapHolder()
    env.sniff(heapHolder)

def test_sniff_no_class_found_public():
    env = EnvProperty01()
    class Dummy(PublicDummyHeapHolder):
        def findClass(self, var1): return None
    heapHolder = Dummy()
    assert env.sniff(heapHolder) is None