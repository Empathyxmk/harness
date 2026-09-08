from src.mfit_summary import mfit_summary
import numpy as np

def test_basic_summary(capsys):
    results = dict()
    results['param'] = [dict(name='alpha'), dict(name='beta')]
    results['x'] = np.array([[1,3],[2,1],[3,5],[4,2]])
    def bootfun(x):
        return np.mean(x)
    nboot = 10
    mfit_summary(results, bootfun, nboot)
    out = capsys.readouterr().out
    assert "Param alpha" in out and "Param beta" in out

def test_default_params(capsys):
    results = dict(param=[{'name':'alpha'}], x=np.arange(1,11)[:,None])
    mfit_summary(results)
    out = capsys.readouterr().out
    assert "Param alpha" in out

def test_empty_bootfun(capsys):
    results = dict(param=[{'name':'gamma'}], x=np.arange(2,12)[:,None])
    mfit_summary(results, None, 7)
    out = capsys.readouterr().out
    assert "Param gamma" in out

def test_empty_nboot(capsys):
    results = dict(param=[{'name':'delta'}], x=np.arange(3,13)[:,None])
    mfit_summary(results, np.mean, None)
    out = capsys.readouterr().out
    assert "Param delta" in out