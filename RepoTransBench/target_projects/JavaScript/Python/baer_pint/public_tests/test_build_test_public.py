import os
import shutil
import pytest

build_test_dir = os.path.join(os.path.dirname(__file__), '..', '.build_test_public')
test_file = os.path.join(build_test_dir, 'foo.test.js')

@pytest.fixture(autouse=True, scope='module')
def setup_and_cleanup():
    os.makedirs(build_test_dir, exist_ok=True)
    with open(test_file, 'w') as f:
        f.write('// build public test')
    yield
    if os.path.exists(test_file):
        os.remove(test_file)
    if os.path.exists(build_test_dir):
        try:
            os.rmdir(build_test_dir)
        except OSError:
            shutil.rmtree(build_test_dir, ignore_errors=True)

def test_create_public_build_test_file():
    assert os.path.exists(test_file)
    with open(test_file, 'r') as f:
        content = f.read()
    assert 'public' in content

def test_cleanup_public_build_test_directory():
    if os.path.exists(test_file):
        os.remove(test_file)
    assert not os.path.exists(test_file)
    # Restore for fixture cleanup
    with open(test_file, 'w') as f:
        f.write('// build public test')