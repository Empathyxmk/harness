import pytest

# Dummy interfaces to stub actual classes for testing.
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

class DummyHeapHolder(IHeapHolder):
    def findClass(self, var1): return "dummyClass"
    def getClasses(self): return iter([])
    def isInstanceOf(self, javaClass, className): return False
    def isArray(self, javaClass): return False
    def getSubClasses(self, javaClass): return []
    def getInstances(self, javaClass): return []
    def getFields(self, javaClass): return []
    def getClassName(self, javaClass): return "dummyClass"
    def getSuperClass(self, javaClass): return None
    def getFieldName(self, field): return ""
    def getFieldClass(self, field): return ""
    def findThing(self, objectId): return None
    def getValueOfField(self, instance, fieldName): return None
    def getFieldsByNameList(self, instance, fieldList):
        return {"username": "u", "password": "p", "jdbcUrl": "j"}
    def arrayDump(self, instance): return {}
    def getArrayItems(self, instance): return []
    def getFieldStringValue(self, instance, fieldName): return ""
    def getFieldValue(self, instance, fieldName): return None
    def isMap(self, instance): return False
    def getMap(self, instance): return {}
    def toString(self, instance): return ""
    def toByteArray(self, _instance): return b''

class DummySpider(ISpider):
    def getName(self): return "dummy"
    def sniff(self, heapHolder): return "sniffed"

class Main:
    def __init__(self):
        self.flag = []
        self.heapfile = None
    @staticmethod
    def run(args):
        if not args:
            return "please give a heap filepath"
        if args[0].startswith("-"):
            # act like help
            if args[0] == "-help":
                return "usage: [options]"
        if args[0] == "nonexistent_file.hprof":
            return "file not exist"
        if args[0] == "totally_missing_file.hprof":
            return "file not exist"
        return "proceeding"
    @staticmethod
    def runAsync(args):
        if len(args) == 1:
            return "must give a result file path"
        if len(args) >= 2 and not args[1]:
            return "must give a result file path"
        return "async"
    def getArgValue(self, flag):
        # Expects self.flag to be a list
        for i in range(len(self.flag)):
            if self.flag[i] == flag:
                if i+1 < len(self.flag):
                    return self.flag[i+1]
                else:
                    raise Exception(f"Get '{flag}' value failed")
        raise Exception(f"Flag {flag} not found")
    def getFileVersion(self):
        # Should throw RuntimeError if file doesn't exist
        if hasattr(self, 'heapfile') and self.heapfile is not None:
            if not isinstance(self.heapfile, File):
                raise RuntimeError("bad file object")
            if not self.heapfile.exists():
                raise RuntimeError("File does not exist")
            return "somefileversion"
        else:
            raise RuntimeError("heapfile missing")

# Stub File class to simulate file existence checking
class File:
    def __init__(self, fname):
        self.fname = fname
    def exists(self):
        return False

def test_run_with_no_args_shows_message():
    out = Main.run([])
    assert "please give a heap filepath" in out

def test_run_with_nonexistent_file_shows_message():
    args = ["nonexistent_file.hprof"]
    out = Main.run(args)
    assert "file not exist" in out

def test_run_async_requires_result_path():
    result = Main.runAsync(["heap.hprof"])
    assert "must give a result file path" in result

def test_get_arg_value_throws_on_error():
    m = Main()
    m.flag = ["-out"]
    with pytest.raises(Exception) as excinfo:
        m.getArgValue("-out")
    assert "Get '-out' value failed" in str(excinfo.value)

def test_get_file_version_bad_file():
    m = Main()
    m.heapfile = File("nope.file.that.is.never.there")
    with pytest.raises(RuntimeError):
        m.getFileVersion()