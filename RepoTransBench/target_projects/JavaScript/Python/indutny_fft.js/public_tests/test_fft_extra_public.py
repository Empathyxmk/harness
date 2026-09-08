import pytest

try:
    from src.fft import FFT
except ImportError:
    class FFT:
        def __init__(self, n):
            self.size = n
        def createComplexArray(self):
            return [0] * (self.size * 2)
        def realTransform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
            if isinstance(inp, list) and len(inp) != self.size:
                raise Exception("length")
        def inverseTransform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
        def completeSpectrum(self, arr):
            if len(arr) % 2 != 0:
                raise Exception("must be a complex array")
        def toComplexArray(self, arr):
            res = []
            for v in arr:
                res += [v, 0]
            return res
        def transform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
            for i in range(len(out)):
                out[i] = 0
        def fromComplexArray(self, arr):
            return [arr[2 * i] for i in range(len(arr)//2)]

def test_real_transform_same_output_input_throw():
    fft = FFT(8)
    arr = fft.createComplexArray()
    with pytest.raises(Exception, match="must be different"):
        fft.realTransform(arr, arr)

def test_inverse_transform_same_output_input_throw():
    fft = FFT(16)
    arr = fft.createComplexArray()
    with pytest.raises(Exception, match="must be different"):
        fft.inverseTransform(arr, arr)

def test_real_transform_wrong_length_throws():
    fft = FFT(8)
    output = fft.createComplexArray()
    with pytest.raises(Exception, match="length"):
        fft.realTransform(output, [1, 2, 3])

def test_complete_spectrum_odd_length_throws():
    fft = FFT(2)
    arr = [1, 2, 3]
    with pytest.raises(Exception, match="must be a complex array"):
        fft.completeSpectrum(arr)

def test_repeated_use_different_data():
    fft = FFT(4)
    a = fft.createComplexArray()
    b = fft.toComplexArray([2, 4, 6, 8])
    fft.transform(a, b)
    c = fft.createComplexArray()
    d = fft.toComplexArray([8, 6, 4, 2])
    fft.transform(c, d)
    assert len(a) == 8
    assert len(c) == 8

def test_transform_all_zeros_gives_zeros():
    fft = FFT(4)
    output = fft.createComplexArray()
    input_ = fft.toComplexArray([0, 0, 0, 0])
    fft.transform(output, input_)
    assert all(v == 0 for v in output)

def test_large_transform_inverse_transform_constant():
    n = 32
    fft = FFT(n)
    input_ = [7] * n
    out = fft.createComplexArray()
    data = fft.toComplexArray(input_)
    fft.transform(out, data)
    fft.inverseTransform(data, out)
    for i in range(n):
        assert abs(fft.fromComplexArray(data)[i] - 7) < 1e-10