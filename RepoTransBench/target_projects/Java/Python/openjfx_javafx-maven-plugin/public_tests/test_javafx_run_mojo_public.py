import os
import tempfile
import pytest

class MojoExecutionException(Exception):
    pass

class JavaFXRunMojo:
    def __init__(self):
        self.mainClass = None
        self.basedir = None
        self.builddir = None
        self.skip = False
        self._executable = "java"

    def execute(self):
        if getattr(self, 'skip', False):
            return
        # forcibly simulate null executable
        if getattr(self, '_executable', None) is None:
            raise MojoExecutionException("Executable is null")

def _set_private_executable_null(obj):
    obj._executable = None

@pytest.fixture
def mojo():
    m = JavaFXRunMojo()
    m.mainClass = "org.publicexample.Launcher"
    tmpdir = os.path.join(tempfile.gettempdir(), "publictestsubdir_run")
    os.makedirs(tmpdir, exist_ok=True)
    m.basedir = tmpdir
    m.builddir = tmpdir
    return m

def test_execute_throws_when_executable_null(mojo):
    _set_private_executable_null(mojo)
    with pytest.raises(MojoExecutionException):
        mojo.execute()

def test_skip_execution(mojo):
    mojo.skip = True
    mojo.execute()