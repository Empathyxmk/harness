import pytest

# Assume FFT is importable from src.fft
# You MUST implement/port FFT class as needed; here, we mock its interface for tests to run.
try:
    from src.fft import FFT
except ImportError:
    # Fallback mock for FFT interface for linting/test stubbing; replace with actual.
    class FFT:
        def __init__(self, n):
            pass
        def createComplexArray(self):
            return [0] * (self.size * 2)
        def realTransform(self, out, inp):
            raise NotImplementedError
        def inverseTransform(self, out, inp):
            raise NotImplementedError
        def completeSpectrum(self, arr):
            pass
        def toComplexArray(self, arr, out=None):
            if out is not None:
                out[:len(arr)*2] = [v for x in arr for v in (x, 0)]
                return out
            else:
                return [v for x in arr for v in (x, 0)]
        def fromComplexArray(self, carr, out=None):
            if out is not None:
                for i in range(len(out)):
                    out[i] = carr[2*i]
                return out
            else:
                return [carr[2*i] for i in range(len(carr)//2)]

def test_real_transform_throws_if_same_buffer():
    fft = FFT(4)
    arr = fft.createComplexArray()
    with pytest.raises(Exception, match="must be different"):
        fft.realTransform(arr, arr)

def test_inverse_transform_throws_if_same_buffer():
    fft = FFT(4)
    arr = fft.createComplexArray()
    with pytest.raises(Exception, match="must be different"):
        fft.inverseTransform(arr, arr)

def test_complete_spectrum_even_length_no_throw():
    fft = FFT(4)
    arr = [1, 2, 3, 4, 5, 6, 7, 8]
    fft.completeSpectrum(arr)  # should not throw
    assert len(arr) == 8

def test_to_complex_array_returns_supplied_output():
    fft = FFT(2)
    out = [99, 99, 99, 99]
    res = fft.toComplexArray([1, 2], out)
    assert res is out
    assert out == [1, 0, 2, 0]

def test_from_complex_array_returns_supplied_output():
    fft = FFT(2)
    arr = [1, 0, 2, 0]
    out = [88, 88]
    res = fft.fromComplexArray(arr, out)
    assert res is out
    assert out == [1, 2]

def test_create_complex_array_returns_zeros():
    fft = FFT(8)
    arr = fft.createComplexArray()
    assert len(arr) == 16
    assert all(x == 0 for x in arr)

def test_throws_for_non_power_of_two_size_fft():
    with pytest.raises(Exception, match="power of two"):
        FFT(1)
    with pytest.raises(Exception, match="power of two"):
        FFT(10)
    with pytest.raises(Exception, match="power of two"):
        FFT(-2)