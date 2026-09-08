import pickle

def test_public_pickle_float():
    num = 3.1415
    dumped = pickle.dumps(num)
    loaded = pickle.loads(dumped)
    assert loaded == 3.1415
    assert type(loaded) is float

def test_public_pickle_tuple():
    t = (9, "z", 11.3)
    dumped = pickle.dumps(t)
    loaded = pickle.loads(dumped)
    assert loaded == (9, "z", 11.3)