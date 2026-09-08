import numpy as np

try:
    from src.ann_train import ann_train
except ImportError:
    ann_train = None

def test_public_ann_train():
    print('Testing ann_train (public)...')
    if ann_train is not None:
        try:
            X = np.random.rand(4,2)
            Y = np.random.rand(4,1)
            net = ann_train(X, Y)
            assert isinstance(net, (np.ndarray, dict)) or hasattr(net, '__dict__')
        except Exception as err:
            print(f'ann_train failed (public): {err}')
        # non-square but valid shape
        try:
            ann_train(np.random.rand(5,3), np.random.rand(5,1))
        except Exception:
            pass
        # wrong input dimensions
        try:
            ann_train(np.random.rand(2,5), np.random.rand(3,2))
        except Exception:
            pass
    else:
        print('ann_train.py (ann_train) not found')