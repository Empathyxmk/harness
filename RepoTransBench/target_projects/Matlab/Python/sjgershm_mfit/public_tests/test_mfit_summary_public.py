from src.mfit_summary import mfit_summary
import numpy as np

def test_mean_bootstrap_public(capsys):
    np.random.seed(99)
    results = {'x': np.random.randn(15,1), "param": [dict(name="theta")]}
    mfit_summary(results, np.median, 500)
    out = capsys.readouterr().out
    assert "theta" in out

def test_different_param_names_public(capsys):
    results = {'x': np.array([[1,2],[3,4],[5,6]]), "param":[{'name':'alpha'},{'name':'beta'}]}
    mfit_summary(results, np.mean, 200)
    out = capsys.readouterr().out
    assert "alpha" in out and "beta" in out