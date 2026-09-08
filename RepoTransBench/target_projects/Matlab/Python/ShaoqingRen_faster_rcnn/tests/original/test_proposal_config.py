import numpy as np
import tempfile
import os
import pytest
import scipy.io

def proposal_config(image_means=None, ims_per_batch=1):
    # Dummy conf for testing
    conf = {
        "use_gpu": True, # always set for test
        "ims_per_batch": 1,
    }
    if image_means is not None:
        # Assume path; load
        if isinstance(image_means, str):
            conf["image_means"] = scipy.io.loadmat(image_means)['image_means']
        else:
            conf["image_means"] = image_means
    if ims_per_batch != 1:
        raise AssertionError("currently rpn only supports ims_per_batch == 1")
    return conf

def test_basic_config_defaults():
    conf = proposal_config()
    assert isinstance(conf, dict)
    assert 'use_gpu' in conf
    assert conf['ims_per_batch'] == 1

def test_image_means_file_loading():
    # Save random means to .mat file
    image_means = np.random.rand(3,3,3)
    d = tempfile.TemporaryDirectory()
    matfn = os.path.join(d.name, 'testmeans.mat')
    scipy.io.savemat(matfn, {'image_means': image_means})
    conf = proposal_config(image_means=matfn)
    np.testing.assert_allclose(conf['image_means'], image_means)
    d.cleanup()

def test_ims_per_batch_assert():
    with pytest.raises(AssertionError) as excinfo:
        proposal_config(ims_per_batch=2)
    assert "currently rpn only supports ims_per_batch == 1" in str(excinfo.value)