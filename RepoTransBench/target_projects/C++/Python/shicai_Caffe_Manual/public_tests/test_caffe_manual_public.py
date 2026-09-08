# Translated from: test_caffe_manual_public.cpp

def some_caffe_like_function(a, b):
    # Dummy implementation as in the C++ public test
    return a * b + 1

def test_caffe_manual_public_basics():
    assert some_caffe_like_function(4, 5) == 21      # 4 * 5 + 1
    assert some_caffe_like_function(-2, 3) == -5     # -2 * 3 + 1
    assert some_caffe_like_function(0, 0) == 1       # 0 * 0 + 1
    assert some_caffe_like_function(8, -1) == -7     # 8 * -1 + 1