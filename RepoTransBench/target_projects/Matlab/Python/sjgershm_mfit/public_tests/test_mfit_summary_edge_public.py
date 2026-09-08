from src.mfit_summary import mfit_summary
import numpy as np

def test_single_sample_public(capsys):
    np.random.seed(102)
    results = {'x': 10*np.random.randn(1,2), 'param':[{'name':'param1'},{'name':'param2'}]}
    mfit_summary(results, np.mean, 20)
    out = capsys.readouterr().out
    assert "param1" in out and "param2" in out

def test_bootfun_std_public(capsys):
    np.random.seed(77)
    results = {'x': np.random.randn(12,1), 'param':[{'name':'gamma'}]}
    mfit_summary(results, np.std, 15)
    out = capsys.readouterr().out
    assert "gamma" in out