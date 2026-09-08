import pytest
import pandas as pd
import os
from src.eeg_kaggle.save_sub import save_sub

@pytest.mark.parametrize("plot_on", [0, 1])
def test_file_creation(tmp_path, plot_on):
    test_file_name1 = 'testFile_subj1_seg01.mat'
    test_file_name2 = 'testFile_subj2_seg02.mat'
    file_list_test = pd.DataFrame({
        'File': [test_file_name1, test_file_name2],
        'SubSegID': [1, 2]
    })
    preds = [0.123, 0.987]

    params = {'master': 99, 'plotOn': plot_on}
    expected_file_name = tmp_path / f"Master{params['master']}TestSub.csv"

    if expected_file_name.exists():
        expected_file_name.unlink()

    save_sub(str(tmp_path), file_list_test, preds, params)

    assert expected_file_name.exists(), 'CSV file should be created.'

    df = pd.read_csv(expected_file_name)
    assert df['File'].tolist() == file_list_test['File'].tolist(), 'File names in CSV should match'
    assert pytest.approx(df['Class'].tolist(), rel=1e-5) == preds, 'Class predictions in CSV should match'
    expected_file_name.unlink()