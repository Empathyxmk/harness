import math
import random
import pytest
from src.xiahouzuoxin_fft.zx_math import Complex

CH_NUM = 3
FIFO_SIZE = 32
FIFO_SIZE_DIV2 = 16

x = [[Complex() for _ in range(FIFO_SIZE)] for _ in range(CH_NUM)]

def dummy_peak_check():
    ch = 0
    delay = 0
    temp = 0.0
    max_ = 0.0

    for i in range(FIFO_SIZE):
        x[0][i].real = float(i)
        x[0][i].imag = 0

    max_ = x[ch][0].real * x[ch][0].real + x[ch][0].imag * x[ch][0].imag
    delay = 0
    for i in range(1, 5):
        temp = x[ch][i].real * x[ch][i].real + x[ch][i].imag * x[ch][i].imag
        if temp > max_:
            max_ = temp
            delay = i
    for i in range(FIFO_SIZE - 1, FIFO_SIZE - 5, -1):
        temp = x[ch][i].real * x[ch][i].real + x[ch][i].imag * x[ch][i].imag
        if temp > max_:
            max_ = temp
            delay = i
    if delay > FIFO_SIZE_DIV2:
        delay = delay - FIFO_SIZE

    print(f"[test_xcorr_PEAK_CHECK] delay={delay} max={max_:.2f}")

def guass_rand():
    # Box-Muller
    if not hasattr(guass_rand, "phase"):
        guass_rand.phase = 0
    if not hasattr(guass_rand, "V1"):
        guass_rand.V1 = 0.0
    if not hasattr(guass_rand, "V2"):
        guass_rand.V2 = 0.0
    if not hasattr(guass_rand, "S"):
        guass_rand.S = 0.0
    phase = guass_rand.phase

    if phase == 0:
        while True:
            U1 = random.random()
            U2 = random.random()
            V1 = 2 * U1 - 1
            V2 = 2 * U2 - 1
            S = V1 * V1 + V2 * V2
            if S < 1 and S != 0:
                break
        X = V1 * math.sqrt(-2 * math.log(S) / S)
        guass_rand.V2 = V2
        guass_rand.S = S
        guass_rand.phase = 1
        return X
    else:
        X = guass_rand.V2 * math.sqrt(-2 * math.log(guass_rand.S) / guass_rand.S)
        guass_rand.phase = 0
        return X

def test_dummy_peak_check(capsys):
    dummy_peak_check()

def test_guass_rand(capsys):
    print("[test_guass_rand]", end=" ")
    for i in range(20):
        v = guass_rand()
        print(f"{v:.3f}", end=" ")
    print()