import os
import tempfile
import pytest

class MojoExecutionException(Exception):
    pass

class JavaFXJLinkMojo:
    def __init__(self):
        self.mainClass = None
        self.basedir = None
        self.builddir = None

    def execute(self):
        # Should fail because of incomplete setup
        raise MojoExecutionException("Incomplete setup")

@pytest.fixture
def mojo():
    m = JavaFXJLinkMojo()
    m.mainClass = "org.publicexample.Launcher"
    tmpdir = os.path.join(tempfile.gettempdir(), "publictestsubdir")
    os.makedirs(tmpdir, exist_ok=True)
    m.basedir = tmpdir
    m.builddir = tmpdir
    return m

def test_execute_with_exception(mojo):
    with pytest.raises(MojoExecutionException):
        mojo.execute()