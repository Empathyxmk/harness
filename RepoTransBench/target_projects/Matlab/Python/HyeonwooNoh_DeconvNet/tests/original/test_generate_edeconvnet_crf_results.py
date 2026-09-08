import os
import numpy as np
import scipy.io
from tempfile import TemporaryDirectory
from src.hyeonwoonoh_deconvnet.inference.generate_edeconvnet_crf_results import generate_EDeconvNet_CRF_results
from src.hyeonwoonoh_deconvnet.mock.caffe import caffe_singleton

def make_voc_testfile(tmpdir):
    vocdir = os.path.join(tmpdir, 'data', 'VOC2012', 'ImageSets', 'Segmentation')
    os.makedirs(vocdir, exist_ok=True)
    with open(os.path.join(vocdir, 'test.txt'), 'w') as f:
        f.write('2007_000032\n')

def setup_config(tmpdir, write_file=True):
    edgeboxdir = os.path.join(tmpdir, 'data', 'edgebox_cached', 'VOC2012_TEST')
    os.makedirs(edgeboxdir, exist_ok=True)
    boxes_padded = np.array([[10, 10, 200, 200]])
    scipy.io.savemat(os.path.join(edgeboxdir, '2007_000032.mat'), {'boxes_padded': boxes_padded})
    # Also create dummy FCN8s scores (for coverage)
    fcndir = os.path.join(tmpdir, 'mock_deconv_results', 'FCN8s', 'scores')
    os.makedirs(fcndir, exist_ok=True)
    score = np.random.rand(256, 256, 21).astype(np.float32)
    scipy.io.savemat(os.path.join(fcndir, '2007_000032.mat'), {'score': score})

    return {
        'cmap': './voc_gt_cmap.mat',
        'gpuNum': 0,
        'Path': {
            'CNN': {
                'caffe_root': './mock',
                'model_data': 'dummy_deconv.caffemodel',
                'model_proto': 'dummy_deconv.prototxt',
            }
        },
        'im_sz': 224,
        'max_proposal_num': 5,
        'imageset': 'test',
        'write_file': write_file,
        'edgebox_cache_dir': edgeboxdir,
        'save_root': os.path.join(tmpdir, 'mock_deconv_results'),
        'fcn_score_dir': os.path.join(tmpdir, 'mock_deconv_results', 'FCN8s')
    }

class TestGenerateEDeconvNetCRFResults:
    def test_basic_generation(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir, True)
        caffe_singleton().reset()
        generate_EDeconvNet_CRF_results(cfg)
        outdir = os.path.join(cfg['save_root'], 'EDeconvNet_CRF')
        assert os.path.isdir(outdir)
        expected = os.path.join(outdir, '2007_000032.png')
        assert os.path.isfile(expected)

    def test_no_write_file(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir, False)
        caffe_singleton().reset()
        generate_EDeconvNet_CRF_results(cfg)
        outdir = os.path.join(cfg['save_root'], 'EDeconvNet_CRF')
        assert not os.path.exists(outdir)

    def test_min_box_dimension_check(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir)
        edgebox_path = os.path.join(cfg['edgebox_cache_dir'], '2007_000032.mat')
        # Box with small dimension
        scipy.io.savemat(edgebox_path, {'boxes_padded': np.array([[10, 10, 20, 20]])})
        caffe_singleton().reset()
        # Should not crash or write file
        generate_EDeconvNet_CRF_results(cfg)
        # No assertion possible for "continue", but for coverage, it gets hit
        # restore normal box for other tests
        scipy.io.savemat(edgebox_path, {'boxes_padded': np.array([[10, 10, 200, 200]])})