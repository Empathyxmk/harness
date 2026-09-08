import os
import shutil
import pytest

def restore_caffe_dir(caffe_dir, caffe_temp):
    if os.path.exists(caffe_temp):
        if os.path.exists(caffe_dir):
            shutil.rmtree(caffe_dir)
        shutil.move(caffe_temp, caffe_dir)

def dummy_startup():
    # Simulate startup logic: raise if caffe/matlab is missing
    projectdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    caffe_dir = os.path.join(projectdir, 'external', 'caffe', 'matlab')
    if not os.path.isdir(caffe_dir):
        raise RuntimeError('matcaffe is missing')
    # Otherwise, do nothing (success)

def test_startup_with_missing_caffe(tmp_path):
    curdir = os.path.dirname(os.path.abspath(__file__))
    projectdir = os.path.abspath(os.path.join(curdir, '..', '..'))
    caffe_dir = os.path.join(projectdir, 'external', 'caffe', 'matlab')
    caffe_temp = caffe_dir + '_TEMP_REMOVE'
    if os.path.isdir(caffe_dir):
        shutil.move(caffe_dir, caffe_temp)
    try:
        with pytest.raises(Exception) as excinfo:
            dummy_startup()
        assert "matcaffe is missing" in str(excinfo.value)
    finally:
        restore_caffe_dir(caffe_dir, caffe_temp)

def test_startup_pass(tmp_path):
    curdir = os.path.dirname(os.path.abspath(__file__))
    projectdir = os.path.abspath(os.path.join(curdir, '..', '..'))
    caffe_dir = os.path.join(projectdir, 'external', 'caffe', 'matlab')
    os.makedirs(caffe_dir, exist_ok=True)
    try:
        dummy_startup()
    except Exception as err:
        pytest.fail(f'startup threw unexpectedly: {err}')