import pytest
from src.xiahouzuoxin_fft.zx_math import dsp_max_min_val, scale, zx_cabs, Complex, ones_32, floor_log2_32

def test_dsp_max_min_val_pub(capsys):
    arr1 = [7.3, -4.8, 0.6, 2.2, 9.9]
    max_ = [0.0]
    min_ = [0.0]
    dsp_max_min_val(arr1, 5, max_, min_)
    print(f"[PUBLIC][test_dsp_max_min_val] max={max_[0]:.2f} min={min_[0]:.2f}")

    arr2 = [42.42]
    dsp_max_min_val(arr2, 1, max_, min_)
    print(f"[PUBLIC][test_dsp_max_min_val-singleton] max={max_[0]:.2f} min={min_[0]:.2f}")

    arr3 = [5.0, 5.0, 5.0]
    dsp_max_min_val(arr3, 3, max_, min_)
    print(f"[PUBLIC][test_dsp_max_min_val-allconst] max={max_[0]:.2f} min={min_[0]:.2f}")

def test_scale_pub(capsys):
    arr = [-1.0, 0.0, 1.0, 2.0]
    scale(arr, 2.0, -1.0, 4, 10.0, 20.0)
    print(f"[PUBLIC][test_scale] {' '.join([f'{v:.2f}' for v in arr])}")

    arr2 = [-3.14]
    scale(arr2, -3.14, -3.14, 1, -5.0, 5.0)
    print(f"[PUBLIC][test_scale-singleton] {arr2[0]:.2f}")

    arr3 = [-100, 0, 100]
    scale(arr3, 100.0, -100.0, 3, 0.0, 10.0)
    print(f"[PUBLIC][test_scale-large] {' '.join([f'{v:.2f}' for v in arr3])}")

def test_cabs_pub(capsys):
    x = Complex(6.0, 8.0)
    mag = zx_cabs(x)
    print(f"[PUBLIC][test_cabs] {mag:.2f}")

    x = Complex(1, 0)
    print(f"[PUBLIC][test_cabs-1real] {zx_cabs(x):.2f}")

    x = Complex(-9, 12)
    print(f"[PUBLIC][test_cabs-negdiff] {zx_cabs(x):.2f}")

def test_ones_32_pub(capsys):
    print(f"[PUBLIC][test_ones_32](0xAAAAAAAA) = {ones_32(0xAAAAAAAA)}")
    print(f"[PUBLIC][test_ones_32](0x0F0F0F0F) = {ones_32(0x0F0F0F0F)}")
    print(f"[PUBLIC][test_ones_32](0x33333333) = {ones_32(0x33333333)}")
    print(f"[PUBLIC][test_ones_32](2) = {ones_32(2)}")
    print(f"[PUBLIC][test_ones_32](0x40000000u) = {ones_32(0x40000000)}")

def test_floor_log2_32_pub(capsys):
    print(f"[PUBLIC][test_floor_log2_32]16 = {floor_log2_32(16)}")
    print(f"[PUBLIC][test_floor_log2_32]2 = {floor_log2_32(2)}")
    print(f"[PUBLIC][test_floor_log2_32]255 = {floor_log2_32(255)}")
    print(f"[PUBLIC][test_floor_log2_32]0x40000000 = {floor_log2_32(0x40000000)}")
    print(f"[PUBLIC][test_floor_log2_32]7 = {floor_log2_32(7)}")