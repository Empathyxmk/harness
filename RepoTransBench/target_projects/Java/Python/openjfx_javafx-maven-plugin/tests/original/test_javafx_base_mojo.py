import os
import tempfile
import shutil
import pathlib

import pytest

# Simulating an enum for RuntimePathOption
class RuntimePathOption:
    CLASSPATH = 'CLASSPATH'
    MODULEPATH = 'MODULEPATH'

class JavaFXBaseMojo:
    # Just to simulate interface for createMainClassString
    def execute(self):
        pass

    @staticmethod
    def getParent(path, depth):
        curr = pathlib.Path(path)
        for _ in range(depth):
            if curr.parent == curr:
                return None
            curr = curr.parent
        try:
            if not curr.exists():
                return None
        except Exception:
            return None
        return curr

    def createMainClassString(self, mainClass, moduleDescriptor, runtimePath):
        # The test logic is to choose prefix
        if runtimePath == RuntimePathOption.CLASSPATH:
            return mainClass if '/' not in mainClass else mainClass.split('/')[-1]
        if runtimePath == RuntimePathOption.MODULEPATH:
            if moduleDescriptor:
                mod_name = getattr(moduleDescriptor, 'name', 'hellofx')
                if '/' in mainClass:
                    return mainClass
                else:
                    return f"{mod_name}/{mainClass}"
            else:
                return mainClass if '/' not in mainClass else mainClass
        if moduleDescriptor:
            mod_name = getattr(moduleDescriptor, 'name', 'hellofx')
            if '/' not in mainClass:
                return f"{mod_name}/{mainClass}"
            else:
                return mainClass
        # Default
        return mainClass

class DummyModuleDescriptor:
    def __init__(self, name):
        self.name = name

@pytest.fixture(scope='module')
def temp_test_dir():
    tempdir = tempfile.gettempdir()
    testpath = os.path.join(tempdir, 'test', 'test')
    os.makedirs(testpath, exist_ok=True)
    yield pathlib.Path(testpath)
    # Cleanup
    parent_dir = pathlib.Path(testpath).parent
    if parent_dir.exists():
        for root, dirs, files in os.walk(str(parent_dir), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                try:
                    if name == 'test':
                        shutil.rmtree(os.path.join(root, name))
                except Exception:
                    pass

@pytest.fixture
def mojo():
    m = JavaFXBaseMojo()
    return m

@pytest.fixture
def module_descriptor():
    return DummyModuleDescriptor('hellofx')

def test_parent(temp_test_dir):
    tempdir = tempfile.gettempdir()
    assert JavaFXBaseMojo.getParent(temp_test_dir, 2) == pathlib.Path(tempdir)

def test_main_class_string_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('org.openjfx.Main', module_descriptor, None) == 'hellofx/org.openjfx.Main'

def test_main_class_string_without_module_descriptor(mojo):
    assert mojo.createMainClassString('org.openjfx.Main', None, None) == 'org.openjfx.Main'
    assert mojo.createMainClassString('hellofx/org.openjfx.Main', None, None) == 'hellofx/org.openjfx.Main'

def test_main_class_string_with_classpath_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('org.openjfx.Main', module_descriptor, RuntimePathOption.CLASSPATH) == 'org.openjfx.Main'
    assert mojo.createMainClassString('hellofx/org.openjfx.Main', module_descriptor, RuntimePathOption.CLASSPATH) == 'org.openjfx.Main'

def test_main_class_string_with_classpath_without_module_descriptor(mojo):
    assert mojo.createMainClassString('org.openjfx.Main', None, RuntimePathOption.CLASSPATH) == 'org.openjfx.Main'
    assert mojo.createMainClassString('hellofx/org.openjfx.Main', None, RuntimePathOption.CLASSPATH) == 'org.openjfx.Main'

def test_main_class_string_with_modulepath_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('org.openjfx.Main', module_descriptor, RuntimePathOption.MODULEPATH) == 'hellofx/org.openjfx.Main'
    assert mojo.createMainClassString('hellofx/org.openjfx.Main', module_descriptor, RuntimePathOption.MODULEPATH) == 'hellofx/org.openjfx.Main'

def test_main_class_string_with_modulepath_without_module_descriptor(mojo):
    assert mojo.createMainClassString('org.openjfx.Main', None, RuntimePathOption.MODULEPATH) == 'org.openjfx.Main'
    assert mojo.createMainClassString('hellofx/org.openjfx.Main', None, RuntimePathOption.MODULEPATH) == 'hellofx/org.openjfx.Main'

def test_invalid_parent(temp_test_dir):
    assert JavaFXBaseMojo.getParent(temp_test_dir, 10) is None

def test_invalid_path():
    assert JavaFXBaseMojo.getParent(pathlib.Path('/some-invalid-path'), 0) is None

def test_invalid_path_with_depth():
    assert JavaFXBaseMojo.getParent(pathlib.Path('/some-invalid-path'), 2) is None