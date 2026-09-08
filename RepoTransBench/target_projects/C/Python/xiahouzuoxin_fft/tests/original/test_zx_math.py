import pytest
from src.xiahouzuoxin_fft.zx_math import dsp_max_min_val, scale, zx_cabs, Complex, ones_32, floor_log2_32

def test_dsp_max_min_val(capsys):
    arr1 = [1.5, 2.5, -3.5, 8.2, 0.0]
    max_ = [0.0]
    min_ = [0.0]
    dsp_max_min_val(arr1, 5, max_, min_)
    print(f"[test_dsp_max_min_val] max={max_[0]:.2f} min={min_[0]:.2f}")

    arr2 = [0.0]
    dsp_max_min_val(arr2, 1, max_, min_)
    print(f"[test_dsp_max_min_val-singleton] max={max_[0]:.2f} min={min_[0]:.2f}")

    arr3 = [-2.0, -2.0, -2.0]
    dsp_max_min_val(arr3, 3, max_, min_)
    print(f"[test_dsp_max_min_val-allneg] max={max_[0]:.2f} min={min_[0]:.2f}")

def test_scale(capsys):
    arr = [2.0, 4.0, 6.0, 8.0]
    scale(arr, 8.0, 2.0, 4, -1.0, 1.0)
    print(f"[test_scale] {' '.join([f'{v:.2f}' for v in arr])}")

    arr2 = [3.14]
    scale(arr2, 3.14, 3.14, 1, 0.0, 1.0)
    print(f"[test_scale-singleton] {arr2[0]:.2f}")

    arr3 = [0, 50, 100]
    scale(arr3, 100.0, 0.0, 3, -100.0, 100.0)
    print(f"[test_scale-large] {' '.join([f'{v:.2f}' for v in arr3])}")

def test_cabs(capsys):
    x = Complex(3.0, 4.0)
    mag = zx_cabs(x)
    print(f"[test_cabs] {mag:.2f}")

    x = Complex(0.0, 0.0)
    print(f"[test_cabs-zero] {zx_cabs(x):.2f}")

    x = Complex(-5.0, 12.0)
    print(f"[test_cabs-neg] {zx_cabs(x):.2f}")

def test_ones_32(capsys):
    print(f"[test_ones_32](0) = {ones_32(0)}")
    print(f"[test_ones_32](0xFFFFFFFF) = {ones_32(0xFFFFFFFF)}")
    print(f"[test_ones_32](0xF0F0) = {ones_32(0xF0F0)}")
    print(f"[test_ones_32](1) = {ones_32(1)}")
    print(f"[test_ones_32](0x80000000u) = {ones_32(0x80000000)}")

def test_floor_log2_32(capsys):
    print(f"[test_floor_log2_32]8 = {floor_log2_32(8)}")
    print(f"[test_floor_log2_32]1 = {floor_log2_32(1)}")
    print(f"[test_floor_log2_32]1023 = {floor_log2_32(1023)}")
    print(f"[test_floor_log2_32]0x80000000 = {floor_log2_32(0x80000000)}")
    print(f"[test_floor_log2_32]3 = {floor_log2_32(3)}")