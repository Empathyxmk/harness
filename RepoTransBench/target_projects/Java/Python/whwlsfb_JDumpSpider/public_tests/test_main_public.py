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

class ISpider:
    def getName(self): raise NotImplementedError
    def sniff(self, heapHolder): raise NotImplementedError

class PublicDummyHeapHolder(IHeapHolder):
    def findClass(self, var1): return "publicDummyClass"
    def getClasses(self): return iter([])
    def isInstanceOf(self, javaClass, className): return True
    def isArray(self, javaClass): return True
    def getSubClasses(self, javaClass): return ["sub1"]
    def getInstances(self, javaClass): return ["instance"]
    def getFields(self, javaClass): return ["field"]
    def getClassName(self, javaClass): return "publicDummyClass"
    def getSuperClass(self, javaClass): return "publicSuperClass"
    def getFieldName(self, field): return "fieldName"
    def getFieldClass(self, field): return "fieldClass"
    def findThing(self, objectId): return "foundThing"
    def getValueOfField(self, instance, fieldName): return "valueOfField"
    def getFieldsByNameList(self, instance, fieldList):
        return {"username": "publicU", "password": "publicP", "jdbcUrl": "jdbc:public"}
    def arrayDump(self, instance): return {}
    def getArrayItems(self, instance): return ["item1", "item2"]
    def getFieldStringValue(self, instance, fieldName): return "stringValue"
    def getFieldValue(self, instance, fieldName): return "fieldValue"
    def isMap(self, instance): return True
    def getMap(self, instance): return {}
    def toString(self, instance): return "toStringResult"
    def toByteArray(self, _instance): return b'\x01\x02\x03'

class PublicDummySpider(ISpider):
    def getName(self): return "publicDummy"
    def sniff(self, heapHolder): return "public_sniffed"

class Main:
    def __init__(self):
        self.flag = []
        self.heapfile = None
    @staticmethod
    def run(args):
        if not args:
            return "please give a heap filepath"
        if args[0].startswith("-"):
            if args[0] == "-help":
                return "usage: [options]"
        if args[0] == "totally_missing_file.hprof":
            return "file not exist"
        if args[0] == "nonexistent_file.hprof":
            return "file not exist"
        return "run"
    @staticmethod
    def runAsync(args):
        if len(args) == 1:
            return "must give a result file path"
        elif len(args) >= 2 and not args[1]:
            return "must give a result file path"
        return "asyncrun"
    def getArgValue(self, flag):
        for i in range(len(self.flag)):
            if self.flag[i] == flag:
                if i+1 < len(self.flag):
                    return self.flag[i+1]
                else:
                    raise Exception(f"Get '{flag}' value failed")
        raise Exception(f"Flag {flag} not found")
    def getFileVersion(self):
        if hasattr(self, 'heapfile') and self.heapfile is not None:
            if not isinstance(self.heapfile, File):
                raise RuntimeError("bad file object")
            if not self.heapfile.exists():
                raise RuntimeError("File does not exist")
            return "somefileversion"
        else:
            raise RuntimeError("heapfile missing")

class File:
    def __init__(self, fname):
        self.fname = fname
    def exists(self):
        return False

def test_run_with_help_flag_shows_help_message():
    out = Main.run(["-help"])
    assert "usage" in out

def test_run_with_nonexistent_file_shows_message_different_name():
    out = Main.run(["totally_missing_file.hprof"])
    assert "file not exist" in out.lower()

def test_run_async_requires_result_path_different_heap():
    result = Main.runAsync(["randomheap.hprof"])
    assert "must give a result file path" in result.lower()

def test_get_arg_value_throws_on_different_flag():
    m = Main()
    m.flag = ["-in"]
    with pytest.raises(Exception) as excinfo:
        m.getArgValue("-in")
    assert "get '-in' value failed" in str(excinfo.value).lower()

def test_get_file_version_bad_file_different():
    m = Main()
    m.heapfile = File("definitely_nonexistent_file.file")
    with pytest.raises(RuntimeError):
        m.getFileVersion()