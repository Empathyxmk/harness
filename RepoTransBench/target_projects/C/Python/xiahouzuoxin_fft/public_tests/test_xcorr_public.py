import pytest
from src.xiahouzuoxin_fft.zx_math import Complex

CH_NUM = 3
FIFO_SIZE = 32
FIFO_SIZE_DIV2 = 16

x = [[Complex() for _ in range(FIFO_SIZE)] for _ in range(CH_NUM)]

def dummy_peak_check_pub():
    ch = 1
    delay = 0
    temp = 0.0
    max_ = 0.0
    # Fill ch 1 with values in reverse order
    for i in range(FIFO_SIZE):
        x[1][i].real = float(31-i)
        x[1][i].imag = 0

    max_ = x[ch][0].real * x[ch][0].real + x[ch][0].imag * x[ch][0].imag
    delay = 0
    for i in range(1, 10):
        temp = x[ch][i].real * x[ch][i].real + x[ch][i].imag * x[ch][i].imag
        if temp > max_:
            max_ = temp
            delay = i
    for i in range(FIFO_SIZE-1, FIFO_SIZE-10, -1):
        temp = x[ch][i].real * x[ch][i].real + x[ch][i].imag * x[ch][i].imag
        if temp > max_:
            max_ = temp
            delay = i
    if delay > FIFO_SIZE_DIV2:
        delay = delay - FIFO_SIZE
    print(f"[PUBLIC][dummy_peak_check] ch={ch} peak_idx={delay} max={max_:.2f}")

def dummy_conj_pub():
    for i in range(FIFO_SIZE):
        x[0][i].real = float(i % 5)
        x[0][i].imag = float((i%3) - 1)
        x[2][i].real = float((31-i) % 7)
        x[2][i].imag = float((i%4)-2)
    idx = 15
    conj_real = x[0][idx].real * x[2][idx].real + x[0][idx].imag * x[2][idx].imag
    conj_imag = x[0][idx].real * x[2][idx].imag - x[0][idx].imag * x[2][idx].real
    print(f"[PUBLIC][dummy_conj] idx={idx} conj_real={conj_real:.2f} conj_imag={conj_imag:.2f}")

def test_dummy_peak_check_pub(capsys):
    dummy_peak_check_pub()

def test_dummy_conj_pub(capsys):
    dummy_conj_pub()