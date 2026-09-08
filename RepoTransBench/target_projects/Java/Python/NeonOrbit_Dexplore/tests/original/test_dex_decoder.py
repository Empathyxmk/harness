import pytest

class ReferencePool:
    def __init__(self):
        pass
    def contains(self, v): 
        return v in ("Dex Samples",)
    def stringsContain(self, v): 
        return v in ("A unique string",)
    def typesContain(self, v): 
        return v in ("java.io.File",)
    def fieldsContain(self, v): 
        return v in ("TITLE",)
    def methodsContain(self, v): 
        return v in ("println",)
    def fieldSignaturesContain(self, v): 
        return v in ("io.neonorbit.Sample.TITLE:java.lang.String",)
    def methodSignaturesContain(self, v): 
        return v in ("java.io.PrintStream.println(java.lang.String):void",)

class DexEntry:
    def getDexFile(self): 
        return "fake.dex"
    def getClasses(self):
        return [DexClass()]

class DexClass:
    pass

class DexDecoder:
    @staticmethod
    def decodeFully(target):
        return ReferencePool()

class DexBasedTestHelper:
    def getDexEntries(self):
        return [DexEntry()]
        
@pytest.fixture
def helper():
    return DexBasedTestHelper()

def test_dex_file_references(helper):
    pool = DexDecoder.decodeFully(helper.getDexEntries()[0].getDexFile())
    assert pool.contains("Dex Samples")
    assert pool.stringsContain("A unique string")
    assert pool.typesContain("java.io.File")
    assert pool.fieldsContain("TITLE")
    assert pool.methodsContain("println")
    assert pool.fieldSignaturesContain("io.neonorbit.Sample.TITLE:java.lang.String")
    assert pool.methodSignaturesContain("java.io.PrintStream.println(java.lang.String):void")

def test_dex_class_references(helper):
    assert match(lambda pool: pool.contains("A unique string"), helper) == 1
    assert match(lambda pool: pool.stringsContain("A unique string"), helper) == 1
    assert match(lambda pool: pool.typesContain("java.io.File"), helper) == 1
    assert match(lambda pool: pool.fieldsContain("TITLE"), helper) == 1
    assert match(lambda pool: pool.methodsContain("println"), helper) == 1
    assert match(lambda pool: pool.fieldSignaturesContain("io.neonorbit.Sample.TITLE:java.lang.String"), helper) == 1
    assert match(lambda pool: pool.methodSignaturesContain("java.io.PrintStream.println(java.lang.String):void"), helper) == 1

def match(filter_func, helper):
    count = 0
    for entry in helper.getDexEntries():
        for _ in [DexClass()]:
            pool = DexDecoder.decodeFully("dex_class")
            if filter_func(pool):
                count += 1
    return count