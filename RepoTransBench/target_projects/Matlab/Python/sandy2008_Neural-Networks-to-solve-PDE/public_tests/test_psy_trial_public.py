from src.pde_utils.psy_trial import psy_trial

def test_psy_trial_public_A():
    x1 = [0.5, 0.3]
    NNresult1 = 0.7
    result1 = psy_trial(x1, NNresult1)
    x, t = x1[0], x1[1]
    expected1 = x * (1 - x) * t + x * (1 - x) * t * (1 - t) * NNresult1
    assert abs(result1 - expected1) < 1e-6

def test_psy_trial_public_B():
    x2 = [0.1, 0.9]
    NNresult2 = 0.2
    result2 = psy_trial(x2, NNresult2)
    x, t = x2[0], x2[1]
    expected2 = x * (1 - x) * t + x * (1 - x) * t * (1 - t) * NNresult2
    assert abs(result2 - expected2) < 1e-6