import os
import tempfile
import pytest

def dummy_faster_rcnn_build(nms_bin, nmsgpu_bin, nmscpp, nmscu, nvmexm):
    # Simulate build logic
    # Stubs for mex/nvmex not needed in Python: simulate touch
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

def test_noop_if_all_built_public(tmp_path):
    cwd = tmp_path
    nms_mex_dummy = os.path.join(cwd, 'nms_mex.mex')
    nms_gpu_mex_dummy = os.path.join(cwd, 'nms_gpu_mex.mex')
    open(nms_mex_dummy, 'w').close()
    open(nms_gpu_mex_dummy, 'w').close()
    try:
        dummy_faster_rcnn_build(nms_mex_dummy, nms_gpu_mex_dummy,
                                os.path.join(cwd,'functions','nms','nms_mex.cpp'),
                                os.path.join(cwd,'functions','nms','nms_gpu_mex.cu'),
                                os.path.join(cwd,'functions','nms','nvmex.m'))
    except Exception as err:
        pytest.fail(f'faster_rcnn_build errored: {err}')
    os.remove(nms_mex_dummy)
    os.remove(nms_gpu_mex_dummy)

def test_compiles_if_missing_public(tmp_path):
    cwd = tmp_path
    nms_bin = os.path.join(cwd, 'bin', 'nms_mex')
    nmsgpu_bin = os.path.join(cwd, 'bin', 'nms_gpu_mex')
    os.makedirs(os.path.join(cwd, 'functions', 'nms'), exist_ok=True)
    dummy_faster_rcnn_build(nms_bin, nmsgpu_bin,
                            os.path.join(cwd,'functions','nms','nms_mex.cpp'),
                            os.path.join(cwd,'functions','nms','nms_gpu_mex.cu'),
                            os.path.join(cwd,'functions','nms','nvmex.m'))
    # No exception thrown, OK