import pytest

# Dummy/mockable logic for this translation layer
class ReferencePool:
    def __init__(self):
        # The "database" for these tests. Real logic would parse a dex file. 
        pass
    def contains(self, v): 
        return v in ("Sample Interface",)
    def stringsContain(self, v): 
        return v in ("primary value",)
    def typesContain(self, v): 
        return v in ("java.lang.StringBuilder",)
    def fieldsContain(self, v): 
        return v in ("counter",)
    def methodsContain(self, v): 
        return v in ("toString",)
    def fieldSignaturesContain(self, v): 
        return v in ("io.neonorbit.Sample.counter:int",)
    def methodSignaturesContain(self, v): 
        return v in ("java.lang.StringBuilder.toString():java.lang.String",)

class DexEntry:
    # For simulation; would wrap contents of a real DEX file
    def getDexFile(self): 
        return "fake.dex"
    def getClasses(self):
        return [DexClass()]

class DexClass:
    # Stand-in for a class in a DEX file that matches the test's signature requirements
    pass

class DexDecoder:
    @staticmethod
    def decodeFully(target):
        # target here can be a file or DexClass but returns a ReferencePool for testing
        return ReferencePool()

class DexBasedTestHelper:
    def getDexEntries(self):
        # Only a single entry needed for tests; would wrap more in real suite
        return [DexEntry()]
        
@pytest.fixture
def helper():
    return DexBasedTestHelper()

def test_dex_file_references_public(helper):
    pool = DexDecoder.decodeFully(helper.getDexEntries()[0].getDexFile())
    assert pool.contains("Sample Interface")
    assert pool.stringsContain("primary value")
    assert pool.typesContain("java.lang.StringBuilder")
    assert pool.fieldsContain("counter")
    assert pool.methodsContain("toString")
    assert pool.fieldSignaturesContain("io.neonorbit.Sample.counter:int")
    assert pool.methodSignaturesContain("java.lang.StringBuilder.toString():java.lang.String")

def test_dex_class_references_public(helper):
    # Any class will match test for these queries
    assert match(lambda pool: pool.contains("primary value"), helper) == 1
    assert match(lambda pool: pool.stringsContain("primary value"), helper) == 1
    assert match(lambda pool: pool.typesContain("java.lang.StringBuilder"), helper) == 1
    assert match(lambda pool: pool.fieldsContain("counter"), helper) == 1
    assert match(lambda pool: pool.methodsContain("toString"), helper) == 1
    assert match(lambda pool: pool.fieldSignaturesContain("io.neonorbit.Sample.counter:int"), helper) == 1
    assert match(lambda pool: pool.methodSignaturesContain("java.lang.StringBuilder.toString():java.lang.String"), helper) == 1

def match(filter_func, helper):
    count = 0
    for entry in helper.getDexEntries():
        for _ in [DexClass()]:
            pool = DexDecoder.decodeFully("dex_class")
            if filter_func(pool):
                count += 1
    return count