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

class DataSource04:
    def getName(self):
        return "AliDruidDataSourceWrapper"

    def sniff(self, heapHolder):
        try:
            found_cls = heapHolder.findClass("AnotherDruidDataSourceWrapper")
            if not found_cls:
                return None
            instances = heapHolder.getInstances(found_cls)
            for instance in instances:
                fields = heapHolder.getFieldsByNameList(instance, {})
                u = fields.get("username")
                p = fields.get("password")
                j = fields.get("jdbcUrl")
                if u and p and j:
                    return f"user: {u}, pass: {p}, jdbc: {j}"
        except Exception:
            pass
        return None

class PublicDummyHeapHolder(IHeapHolder):
    def findClass(self, var1): return self if "AnotherDruidDataSourceWrapper" in var1 else None
    def getClasses(self): return None
    def isInstanceOf(self, javaClass, className): return True
    def isArray(self, javaClass): return True
    def getSubClasses(self, javaClass): return ["pubsub"]
    def getInstances(self, javaClass): return [object(), object()]
    def getFields(self, javaClass): return ["pubfield"]
    def getClassName(self, javaClass): return "pubClazz"
    def getSuperClass(self, javaClass): return None
    def getFieldName(self, field): return ""
    def getFieldClass(self, field): return ""
    def findThing(self, objectId): return None
    def getValueOfField(self, instance, fieldName): return None
    def getFieldsByNameList(self, instance, fieldList):
        return {"username": "pubuser", "password": "pubpass", "jdbcUrl": "jdbc:oracle://newhost/db"}
    def arrayDump(self, instance): return {}
    def getArrayItems(self, instance): return []
    def getFieldStringValue(self, instance, fieldName): return ""
    def getFieldValue(self, instance, fieldName): return None
    def isMap(self, instance): return False
    def getMap(self, instance): return None
    def toString(self, instance): return ""
    def toByteArray(self, _instance): return b''

def test_get_name_public():
    ds = DataSource04()
    assert ds.getName() == "AliDruidDataSourceWrapper"

def test_sniff_no_class_found_public():
    ds = DataSource04()
    class Dummy(IHeapHolder):
        def findClass(self, var1): return None
        def getClasses(self): return None
        def isInstanceOf(self, javaClass, className): return False
        def isArray(self, javaClass): return False
        def getSubClasses(self, javaClass): return []
        def getInstances(self, javaClass): return []
        def getFields(self, javaClass): return []
        def getClassName(self, javaClass): return None
        def getSuperClass(self, javaClass): return None
        def getFieldName(self, field): return None
        def getFieldClass(self, field): return None
        def findThing(self, objectId): return None
        def getValueOfField(self, instance, fieldName): return None
        def getFieldsByNameList(self, instance, fieldList): return {}
        def arrayDump(self, instance): return {}
        def getArrayItems(self, instance): return []
        def getFieldStringValue(self, instance, fieldName): return None
        def getFieldValue(self, instance, fieldName): return None
        def isMap(self, instance): return False
        def getMap(self, instance): return None
        def toString(self, instance): return None
        def toByteArray(self, _instance): return b''
    dummy = Dummy()
    assert ds.sniff(dummy) is None

def test_sniff_happy_path_public():
    ds = DataSource04()
    heapHolder = PublicDummyHeapHolder()
    result = ds.sniff(heapHolder)
    assert "pubuser" in result
    assert "pubpass" in result
    assert "jdbc:oracle://newhost/db" in result

def test_sniff_handles_exception_public():
    ds = DataSource04()
    class ExceptionHeapHolder(PublicDummyHeapHolder):
        def getInstances(self, javaClass):
            raise RuntimeError("publicFail")
    heapHolder = ExceptionHeapHolder()
    # Should not raise!
    ds.sniff(heapHolder)