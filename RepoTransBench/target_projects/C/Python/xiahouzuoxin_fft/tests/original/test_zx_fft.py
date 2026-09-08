import math
import pytest
from src.xiahouzuoxin_fft.zx_fft import fft, ifft, fft_real, ifft_real
from src.xiahouzuoxin_fft.zx_math import Complex

def fill_simple(x, N):
    for i in range(N):
        x[i].real = float(i)
        x[i].imag = 0.0

def test_fft_ifft_identity(capsys):
    N = 8
    x = [Complex() for _ in range(N)]
    fill_simple(x, N)
    fft(x, N)
    ifft(x, N)
    print("[test_fft_ifft_identity]", end=" ")
    for i in range(N):
        print(f"({x[i].real:.2f} {x[i].imag:.2f})", end=" ")
    print()

def test_fft_real_ifft_real(capsys):
    N = 8
    x = [Complex() for _ in range(N)]
    for i in range(N):
        x[i].real = math.cos(2 * math.pi * i / N)
        x[i].imag = 0.0
    fft_real(x, N)
    ifft_real(x, N)
    print("[test_fft_real_ifft_real]", end=" ")
    for i in range(N):
        print(f"({x[i].real:.2f} {x[i].imag:.2f})", end=" ")
    print()

def test_fft_small(capsys):
    N = 2
    x = [Complex() for _ in range(N)]
    x[0].real = 1; x[0].imag = 0
    x[1].real = 0; x[1].imag = 0
    fft(x, N)
    print(f"[test_fft_small] ({x[0].real:.2f} {x[0].imag:.2f}) ({x[1].real:.2f} {x[1].imag:.2f})")

def test_fft_n1(capsys):
    N = 1
    x = [Complex() for _ in range(N)]
    x[0].real = 5.0; x[0].imag = -2.0
    fft(x, N)
    print(f"[test_fft_n1] ({x[0].real:.2f} {x[0].imag:.2f})")

def test_fft_power_of_two_edges(capsys):
    for N in [4, 16]:
        x = [Complex() for _ in range(N)]
        for i in range(N):
            x[i].real = i*0.5
            x[i].imag = -1.0 if i==2 else 0.0
        fft(x, N)
        print(f"[test_fft_power_of_two_edges_N{N}]", end='')
        for i in range(N):
            print(f" ({x[i].real:.2f} {x[i].imag:.2f})", end='')
        print()