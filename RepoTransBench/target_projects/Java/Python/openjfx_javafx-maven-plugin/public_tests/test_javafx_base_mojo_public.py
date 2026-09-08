import os
import tempfile
import shutil
import pathlib

import pytest

class RuntimePathOption:
    CLASSPATH = 'CLASSPATH'
    MODULEPATH = 'MODULEPATH'

class JavaFXBaseMojo:
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
        if runtimePath == RuntimePathOption.CLASSPATH:
            return mainClass if '/' not in mainClass else mainClass.split('/')[-1]
        if runtimePath == RuntimePathOption.MODULEPATH:
            if moduleDescriptor:
                mod_name = getattr(moduleDescriptor, 'name', 'publicmodule')
                if '/' in mainClass:
                    return mainClass
                else:
                    return f"{mod_name}/{mainClass}"
            else:
                return mainClass if '/' not in mainClass else mainClass
        if moduleDescriptor:
            mod_name = getattr(moduleDescriptor, 'name', 'publicmodule')
            if '/' not in mainClass:
                return f"{mod_name}/{mainClass}"
            else:
                return mainClass
        return mainClass

class DummyModuleDescriptor:
    def __init__(self, name):
        self.name = name

@pytest.fixture(scope='module')
def temp_public_test_dir():
    tempdir = tempfile.gettempdir()
    testpath = os.path.join(tempdir, 'publictest', 'pubdir')
    os.makedirs(testpath, exist_ok=True)
    yield pathlib.Path(testpath)
    parent_dir = pathlib.Path(testpath).parent
    if parent_dir.exists():
        for root, dirs, files in os.walk(str(parent_dir), topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                try:
                    if name == 'publictest':
                        shutil.rmtree(os.path.join(root, name))
                except Exception:
                    pass

@pytest.fixture
def mojo():
    m = JavaFXBaseMojo()
    return m

@pytest.fixture
def module_descriptor():
    return DummyModuleDescriptor('publicmodule')

def test_parent(temp_public_test_dir):
    tempdir = tempfile.gettempdir()
    assert JavaFXBaseMojo.getParent(temp_public_test_dir, 2) == pathlib.Path(tempdir)

def test_main_class_string_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('com.publicexample.Main', module_descriptor, None) == 'publicmodule/com.publicexample.Main'

def test_main_class_string_without_module_descriptor(mojo):
    assert mojo.createMainClassString('com.publicexample.Main', None, None) == 'com.publicexample.Main'
    assert mojo.createMainClassString('publicmodule/com.publicexample.Main', None, None) == 'publicmodule/com.publicexample.Main'

def test_main_class_string_with_classpath_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('com.publicexample.Main', module_descriptor, RuntimePathOption.CLASSPATH) == 'com.publicexample.Main'
    assert mojo.createMainClassString('publicmodule/com.publicexample.Main', module_descriptor, RuntimePathOption.CLASSPATH) == 'com.publicexample.Main'

def test_main_class_string_with_classpath_without_module_descriptor(mojo):
    assert mojo.createMainClassString('com.publicexample.Main', None, RuntimePathOption.CLASSPATH) == 'com.publicexample.Main'
    assert mojo.createMainClassString('publicmodule/com.publicexample.Main', None, RuntimePathOption.CLASSPATH) == 'com.publicexample.Main'

def test_main_class_string_with_modulepath_with_module_descriptor(mojo, module_descriptor):
    assert mojo.createMainClassString('com.publicexample.Main', module_descriptor, RuntimePathOption.MODULEPATH) == 'publicmodule/com.publicexample.Main'
    assert mojo.createMainClassString('publicmodule/com.publicexample.Main', module_descriptor, RuntimePathOption.MODULEPATH) == 'publicmodule/com.publicexample.Main'

def test_main_class_string_with_modulepath_without_module_descriptor(mojo):
    assert mojo.createMainClassString('com.publicexample.Main', None, RuntimePathOption.MODULEPATH) == 'com.publicexample.Main'
    assert mojo.createMainClassString('publicmodule/com.publicexample.Main', None, RuntimePathOption.MODULEPATH) == 'publicmodule/com.publicexample.Main'

def test_invalid_parent(temp_public_test_dir):
    assert JavaFXBaseMojo.getParent(temp_public_test_dir, 10) is None

def test_invalid_path():
    assert JavaFXBaseMojo.getParent(pathlib.Path('/some-other-invalid-path'), 0) is None

def test_invalid_path_with_depth():
    assert JavaFXBaseMojo.getParent(pathlib.Path('/some-other-invalid-path'), 2) is None