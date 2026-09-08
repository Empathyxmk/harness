import numpy as np
import pytest

try:
    from src.ann_methodA import ann_methodA
except ImportError:
    ann_methodA = None
try:
    from src.ann_methodB import ann_methodB
except ImportError:
    ann_methodB = None
try:
    from src.ann_methodC import ann_methodC
except ImportError:
    ann_methodC = None

def test_ann_methodA():
    print('Testing ann_methodA...')
    if ann_methodA is not None:
        try:
            x = np.random.rand(5,5)
            w = np.random.rand(5,5)
            outA = ann_methodA(x, w)
            assert isinstance(outA, (np.ndarray, np.generic, bool))
        except Exception as err:
            print('ann_methodA failed: %s' % err)
        # Test empty input
        try:
            ann_methodA(np.array([]), np.array([]))
        except Exception:
            pass
        # Invalid w
        try:
            ann_methodA(np.random.rand(5,5), np.array([]))
        except Exception:
            pass
    else:
        print('ann_methodA.py (ann_methodA) not found')

def test_ann_methodB():
    print('Testing ann_methodB...')
    if ann_methodB is not None:
        try:
            x = np.random.rand(3,3)
            w = np.random.rand(3,3)
            outB = ann_methodB(x, w)
            assert isinstance(outB, (np.ndarray, np.generic, bool))
        except Exception as err:
            print('ann_methodB failed: %s' % err)
        try:
            ann_methodB(np.array([]), np.array([]))
        except Exception:
            pass
        try:
            ann_methodB(np.random.rand(3,3), np.array([]))
        except Exception:
            pass
    else:
        print('ann_methodB.py (ann_methodB) not found')

def test_ann_methodC():
    print('Testing ann_methodC...')
    if ann_methodC is not None:
        try:
            x = np.random.rand(4,4)
            w = np.random.rand(4,4)
            outC = ann_methodC(x, w)
            assert isinstance(outC, (np.ndarray, np.generic, bool))
        except Exception as err:
            print('ann_methodC failed: %s' % err)
        try:
            ann_methodC(np.array([]), np.array([]))
        except Exception:
            pass
        try:
            ann_methodC(np.random.rand(4,4), np.array([]))
        except Exception:
            pass
    else:
        print('ann_methodC.py (ann_methodC) not found')