import pytest
import numpy as np
import pandas as pd
import os
from src.eeg_kaggle.save_sub import save_sub

def test_save_sub_runs_without_error_public(tmp_path):
    Fp = np.random.rand(7,2)
    y = np.array([0, 1, 0, 1, 0, 1, 0])
    params = {}
    params['outFolder'] = str(tmp_path)
    if not os.path.exists(params['outFolder']):
        os.makedirs(params['outFolder'])
    params['subject'] = '333'
    params['fileType'] = 'public_savetype'

    save_sub(Fp, y, params)
    files = [f for f in os.listdir(params['outFolder']) if f.endswith('.mat') or f.endswith('.csv')]
    assert len(files) >= 1

    # cleanup is handled by tmp_path fixture