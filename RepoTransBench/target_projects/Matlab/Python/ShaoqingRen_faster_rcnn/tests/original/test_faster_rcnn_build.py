import os
import tempfile
import shutil
import pytest

def dummy_faster_rcnn_build(nms_bin, nmsgpu_bin, nmscpp, nmscu, nvmexm):
    # Sample logic: (in reality, would compile sources if needed)
    if not os.path.isfile(nms_bin):
        with open(nms_bin, 'w') as f:
            f.write('dummy')
    if not os.path.isfile(nmsgpu_bin):
        with open(nmsgpu_bin, 'w') as f:
            f.write('dummy')
    if not os.path.isfile(nmscpp):
        with open(nmscpp, 'w') as f:
            f.write('int main() {return 0;}')
    if not os.path.isfile(nmscu):
        with open(nmscu, 'w') as f:
            f.write('int main() {return 0;}')
    if not os.path.isfile(nvmexm):
        with open(nvmexm, 'w') as f:
            f.write('function nvmex(varargin); save("nms_gpu_mex."); end')

def test_script_runs_when_no_binaries(tmp_path):
    cwd = tmp_path
    nms_bin = os.path.join(cwd, 'nms_mex.so')
    nmsgpu_bin = os.path.join(cwd, 'nms_gpu_mex.so')
    # Remove if exist (should not exist in tmp_path)
    # Prepare dummy cpp/cu/nvmex files
    os.makedirs(os.path.join(cwd, 'functions', 'nms'), exist_ok=True)
    nmscpp = os.path.join(cwd, 'functions', 'nms', 'nms_mex.cpp')
    nmscu = os.path.join(cwd, 'functions', 'nms', 'nms_gpu_mex.cu')
    nvmexm = os.path.join(cwd, 'functions', 'nms', 'nvmex.m')

    # Remove bins if any exist
    for f in [nms_bin, nmsgpu_bin]:
        try:
            os.remove(f)
        except FileNotFoundError:
            pass

    dummy_faster_rcnn_build(nms_bin, nmsgpu_bin, nmscpp, nmscu, nvmexm)
    try:
        assert os.path.isfile(nms_bin)
        assert os.path.isfile(nmsgpu_bin)
    except Exception as err:
        pytest.fail(f'faster_rcnn_build errored: {err}')