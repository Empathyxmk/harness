import math
import pytest
from src.xiahouzuoxin_fft.zx_fft import fft, ifft, fft_real, ifft_real
from src.xiahouzuoxin_fft.zx_math import Complex

def fill_alternate(x, N):
    for i in range(N):
        x[i].real = float(i) if i % 2 == 0 else -float(i)
        x[i].imag = float((i % 3) - 1)

def test_fft_ifft_identity_pub(capsys):
    N = 8
    x = [Complex() for _ in range(N)]
    fill_alternate(x, N)
    fft(x, N)
    ifft(x, N)
    print("[PUBLIC][test_fft_ifft_identity]", end=" ")
    for i in range(N):
        print(f"({x[i].real:.2f} {x[i].imag:.2f})", end=" ")
    print()

def test_fft_real_ifft_real_pub(capsys):
    N = 8
    x = [Complex() for _ in range(N)]
    for i in range(N):
        x[i].real = math.sin(2 * math.pi * i / (N // 2))
        x[i].imag = 0.0
    fft_real(x, N)
    ifft_real(x, N)
    print("[PUBLIC][test_fft_real_ifft_real]", end=" ")
    for i in range(N):
        print(f"({x[i].real:.2f} {x[i].imag:.2f})", end=" ")
    print()

def test_fft_small_pub(capsys):
    N = 2
    x = [Complex() for _ in range(N)]
    x[0].real = 2
    x[0].imag = 1
    x[1].real = 1
    x[1].imag = -1
    fft(x, N)
    print(f"[PUBLIC][test_fft_small] ({x[0].real:.2f} {x[0].imag:.2f}) ({x[1].real:.2f} {x[1].imag:.2f})")

def test_fft_n1_pub(capsys):
    N = 1
    x = [Complex() for _ in range(N)]
    x[0].real = -3.0
    x[0].imag = 2.0
    fft(x, N)
    print(f"[PUBLIC][test_fft_n1] ({x[0].real:.2f} {x[0].imag:.2f})")

def test_fft_power_of_two_edges_pub(capsys):
    for N in [8, 32]:
        x = [Complex() for _ in range(N)]
        for i in range(N):
            x[i].real = float(i % 5) - 2.0
            x[i].imag = 0.0 if i % 2 == 0 else 1.0
        fft(x, N)
        print(f"[PUBLIC][test_fft_power_of_two_edges_N{N}]", end='')
        for i in range(N):
            print(f" ({x[i].real:.2f} {x[i].imag:.2f})", end='')
        print()