from src.mfit_summary import mfit_summary
import numpy as np

def test_bootfun_sum(capsys):
    results = dict()
    results['param'] = [dict(name='sumstat')]
    results['x'] = np.array([1,2,3,4,5])[:,None]
    mfit_summary(results, np.sum, 5)
    out = capsys.readouterr().out
    assert "sumstat" in out

def test_no_results_param(capsys):
    results = dict()
    results['x'] = np.array([1,2,3,4,5])[:,None]
    results['param'] = [{'name':'pars'}]
    mfit_summary(results, None, 5)
    out = capsys.readouterr().out
    assert "pars" in out