import pytest
import numpy as np
from src.eeg_kaggle.features_object import FeaturesObject

@pytest.fixture(scope="module")
def setup_test_data():
    test_data = np.random.randn(10, 1000)
    test_params = {
        "sampFreq": 200,
        "bands": np.array([[1, 4], [4, 8], [8, 13], [13, 30]]),
        "bandType": "lin",
        "corrType": "pearson",
        "freqRange": [1, 30],
        "n_bins_summ3": 10
    }
    return test_data, test_params

def test_constructor(setup_test_data):
    test_data, _ = setup_test_data
    fobj = FeaturesObject(test_data)
    assert fobj.data.shape == test_data.shape
    assert isinstance(fobj, FeaturesObject)

def test_extract_bands_lin(setup_test_data):
    test_data, test_params = setup_test_data
    fobj = FeaturesObject(test_data)
    extracted = fobj.extract_bands_lin(test_params)
    n_bands = test_params['bands'].shape[0]
    n_channels = test_data.shape[0]
    assert extracted.shape == (n_bands, n_channels)
    assert not np.any(np.isnan(extracted))
    assert not np.any(np.isinf(extracted))

def test_extract_hill_bands(setup_test_data):
    test_data, test_params = setup_test_data
    fobj = FeaturesObject(test_data)
    extracted = fobj.extract_hill_bands(test_params)
    n_bands = test_params['bands'].shape[0]
    n_channels = test_data.shape[0]
    assert extracted.shape == (n_bands, n_channels)
    assert not np.any(np.isnan(extracted))
    assert not np.any(np.isinf(extracted))

def test_extract_channel_correlation_f(setup_test_data):
    test_data, test_params = setup_test_data
    fobj = FeaturesObject(test_data)
    extracted = fobj.extract_channel_correlation_f(test_params)
    n_channels = test_data.shape[0]
    expected_num_corr = n_channels * (n_channels - 1) // 2
    assert extracted.shape == (expected_num_corr, )
    assert not np.any(np.isnan(extracted))
    assert not np.any(np.isinf(extracted))

def test_extract_channel_correlation_t(setup_test_data):
    test_data, test_params = setup_test_data
    fobj = FeaturesObject(test_data)
    extracted = fobj.extract_channel_correlation_t(test_params)
    n_channels = test_data.shape[0]
    expected_num_corr = n_channels * (n_channels - 1) // 2
    assert extracted.shape == (expected_num_corr, )
    assert not np.any(np.isnan(extracted))
    assert not np.any(np.isinf(extracted))

def test_extract_summ3(setup_test_data):
    test_data, test_params = setup_test_data
    fobj = FeaturesObject(test_data)
    extracted = fobj.extract_summ3(test_params)
    n_channels = test_data.shape[0]
    assert len(extracted.shape) == 1
    assert extracted.size > n_channels
    assert not np.any(np.isnan(extracted))
    assert not np.any(np.isinf(extracted))