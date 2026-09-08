from src.libfixmath_python.fix16_fft import four_point_dft, rbit_32

def test_four_point_dft():
    input = [1,2,3,4]
    real = [0,0,0,0]
    imag = [0,0,0,0]
    four_point_dft(input, 1, real, imag)
    assert real[0] != 0
    assert imag[0] == 0
    assert imag[2] == 0

def test_rbit_32():
    assert rbit_32(0b00000000000000000000000000000001) == 0x80000000
    assert rbit_32(0b10101100) != 0

def test_fft_real():
    test_four_point_dft()
    test_rbit_32()