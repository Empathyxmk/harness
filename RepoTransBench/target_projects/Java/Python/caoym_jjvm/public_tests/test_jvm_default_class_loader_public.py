import pytest

# Mock of JvmDefaultClassLoader with error simulation for absent class
class JvmDefaultClassLoader:
    def __init__(self):
        pass

    def loadClass(self, name):
        if name == "org.caoym.nosuch.PublicBogusClass":
            raise ClassNotFoundException("Class PublicBogusClass not found")
        return None

    def getResourceAsStream(self, resourceName):
        return None

class ClassNotFoundException(Exception):
    pass

def test_load_absent_class():
    loader = JvmDefaultClassLoader()
    with pytest.raises(ClassNotFoundException) as ex:
        loader.loadClass("org.caoym.nosuch.PublicBogusClass")
    assert "PublicBogusClass" in str(ex.value)

def test_resource_not_found_public():
    loader = JvmDefaultClassLoader()
    assert loader.getResourceAsStream("public_not_a_resource.txt") is None