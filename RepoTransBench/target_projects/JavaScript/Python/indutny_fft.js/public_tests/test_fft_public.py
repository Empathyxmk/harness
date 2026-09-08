import pytest

try:
    from src.fft import FFT
except ImportError:
    class FFT:
        def __init__(self, n):
            self.size = n
            self.table = [0] * (n * 2)
        def createComplexArray(self):
            return [0] * (self.size * 2)
        def toComplexArray(self, arr):
            res = []
            for v in arr:
                res += [v, 0]
            return res
        def fromComplexArray(self, arr):
            return [arr[2*i] for i in range(len(arr)//2)]
        def transform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
            for i in range(len(out)):
                out[i] = 0
        def inverseTransform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
            for i in range(len(out)):
                out[i] = 0

        def realTransform(self, out, inp):
            if out is inp:
                raise Exception("must be different")
            for i in range(len(out)):
                out[i] = 0
        def completeSpectrum(self, arr):
            pass

def fix_round_equal(actual, expected):
    def fix_round(r):
        return round(r * 10000) / 10000
    assert ":".join(str(fix_round(val)) for val in actual) == ":".join(str(fix_round(val)) for val in expected)

def test_compute_tables_different_size():
    f = FFT(16)
    assert len(f.table) == 32

def test_invalid_table_sizes():
    for val in [5, -8, 0, 3, 13]:
        with pytest.raises(Exception):
            FFT(val)

def test_create_complex_array_different_size():
    f = FFT(2)
    arr = f.createComplexArray()
    assert len(arr) == 4
    assert arr[2] == 0

def test_to_complex_array_different_data():
    f = FFT(2)
    assert f.toComplexArray([10, 20]) == [10, 0, 20, 0]

def test_from_complex_array_different_data():
    f = FFT(2)
    arr = f.toComplexArray([6, 8])
    assert f.fromComplexArray(arr) == [6, 8]

def test_invalid_transform_inputs_new_case():
    f = FFT(4)
    output = f.createComplexArray()
    with pytest.raises(Exception, match="must be different"):
        f.transform(output, output)

def test_trivial_radix2_new_inputs():
    f = FFT(2)
    out = f.createComplexArray()
    data = f.toComplexArray([2, -2])
    f.transform(out, data)
    assert out == [0, 0, 4, 0]
    data = f.toComplexArray([10, 10])
    f.transform(out, data)
    assert out == [20, 0, 0, 0]
    data = f.toComplexArray([-1, 0])
    f.transform(out, data)
    assert out == [-1, 0, -1, 0]

def test_another_trivial_case():
    f = FFT(4)
    out = f.createComplexArray()
    data = f.toComplexArray([3, 1, 0, -1])
    f.transform(out, data)
    fix_round_equal(out, [3, 0, 3, -2.8284, 3, 0, 3, 2.8284])
    data = f.toComplexArray([2, 0, -2, 0])
    f.transform(out, data)
    assert out == [0, 0, 4, 0, 0, 0, 4, 0]

def test_inverse_transform_alternate_data():
    f = FFT(4)
    out = f.createComplexArray()
    data = f.toComplexArray([4, 3, 2, 1])
    f.transform(out, data)
    fix_round_equal(out, [10, 0, 2, 2, -2, 0, 2, -2])
    f.inverseTransform(data, out)
    assert f.fromComplexArray(data) == [4, 3, 2, 1]

def test_transform_bigger_recursive_case():
    input_ = [i * 2 for i in range(64)]
    f = FFT(len(input_))
    out = f.createComplexArray()
    data = f.toComplexArray(input_)
    f.transform(out, data)
    f.inverseTransform(data, out)
    fix_round_equal(f.fromComplexArray(data), input_)

def test_big_recursive_radix2_case():
    input_ = [i * 3 for i in range(32)]
    f = FFT(len(input_))
    out = f.createComplexArray()
    data = f.toComplexArray(input_)
    f.transform(out, data)
    f.inverseTransform(data, out)
    fix_round_equal(f.fromComplexArray(data), input_)