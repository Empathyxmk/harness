import os
import numpy as np
from tempfile import TemporaryDirectory
from src.hyeonwoonoh_deconvnet.inference.cache_fcn8s_results import cache_FCN8s_results
from src.hyeonwoonoh_deconvnet.mock.caffe import caffe_singleton

def make_voc_testfile(tmpdir):
    vocdir = os.path.join(tmpdir, 'data', 'VOC2012', 'ImageSets', 'Segmentation')
    os.makedirs(vocdir, exist_ok=True)
    with open(os.path.join(vocdir, 'test.txt'), 'w') as f:
        f.write('2007_000032\n')

def setup_config(tmpdir, write_file=True):
    return {
        'cmap': './voc_gt_cmap.mat',
        'gpuNum': 0,
        'Path': {
            'CNN': {
                'caffe_root': './mock',
                'model_data': 'dummy.caffemodel',
                'model_proto': 'dummy.prototxt',
            }
        },
        'im_sz': 500,
        'imageset': 'test',
        'write_file': write_file,
        'save_root': os.path.join(tmpdir, 'mock_fcn_results')
    }

class TestCacheFCN8sResults:
    def test_basic_caching(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir, True)
        caffe_singleton().reset()
        cache_FCN8s_results(cfg)
        out_results = os.path.join(cfg['save_root'], 'FCN8s', 'results')
        out_scores = os.path.join(cfg['save_root'], 'FCN8s', 'scores')
        assert os.path.isdir(out_results)
        assert os.path.isdir(out_scores)
        assert os.path.isfile(os.path.join(out_results, '2007_000032.png'))
        assert os.path.isfile(os.path.join(out_scores, '2007_000032.mat'))

    def test_no_write_file(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir, False)
        caffe_singleton().reset()
        cache_FCN8s_results(cfg)
        out_results = os.path.join(cfg['save_root'], 'FCN8s', 'results')
        out_scores = os.path.join(cfg['save_root'], 'FCN8s', 'scores')
        assert not os.path.exists(out_results)
        assert not os.path.exists(out_scores)

    def test_caffe_reset_on_reinit(self, tmp_path):
        tmpdir = str(tmp_path)
        make_voc_testfile(tmpdir)
        cfg = setup_config(tmpdir, True)
        # Manually "init" before test to check reset
        cs = caffe_singleton()
        cs.init('whatever.prototxt', 'whatever.caffemodel')
        assert cs.is_initialized()
        cache_FCN8s_results(cfg)
        # After, should be initialized
        assert caffe_singleton().is_initialized()