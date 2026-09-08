import pytest
from src.izougend_mcmcda.acceptance_pw import acceptance_pw

def test_acceptance_pw_case1():
    mprev = 0
    mcurr = 0
    xsiprev = [0.5]
    xsicurr = [0.8]
    pww1 = 0.6
    pwh1 = 0.3
    expected = min(1, (pwh1 / pww1) * (xsicurr[mcurr] / xsiprev[mprev]))
    P_acc1 = acceptance_pw(pww1, pwh1, xsiprev, xsicurr, mprev, mcurr)
    assert abs(P_acc1 - expected) < 1e-9

def test_acceptance_pw_case2():
    mprev = 0
    mcurr = 0
    xsiprev = [0.1]
    xsicurr = [0.9]
    pww2 = 0.1
    pwh2 = 0.5
    expected = 1
    P_acc2 = acceptance_pw(pww2, pwh2, xsiprev, xsicurr, mprev, mcurr)
    assert abs(P_acc2 - expected) < 1e-9

def test_acceptance_pw_case3():
    mprev = 0
    mcurr = 0
    xsiprev = []
    xsicurr = [0.7]
    pww3 = 0.5
    pwh3 = 0.4
    expected = min(1, (pwh3 / pww3) * (1/1))
    P_acc3 = acceptance_pw(pww3, pwh3, xsiprev, xsicurr, mprev, mcurr)
    assert abs(P_acc3 - expected) < 1e-9

def test_acceptance_pw_case4_zero_pww():
    mprev = 0
    mcurr = 0
    xsiprev = [0.5]
    xsicurr = [0.8]
    pww4 = 0
    pwh4 = 0.3
    P_acc4 = acceptance_pw(pww4, pwh4, xsiprev, xsicurr, mprev, mcurr)
    assert abs(P_acc4 - 1) < 1e-9