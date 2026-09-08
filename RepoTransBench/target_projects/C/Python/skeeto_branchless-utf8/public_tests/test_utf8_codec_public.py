import pytest
from src.utf8.utf8 import utf8_encode, utf8_decode, is_surrogate

def test_decode_sampled():
    for codepoint in range(0x110000)[::8209]:
        if 0xD800 <= codepoint <= 0xDFFF:
            continue
        buf = []
        n = utf8_encode(buf, codepoint)
        if n == 0:
            continue
        val, length, err = utf8_decode(buf)
        assert length == n and val == codepoint and not err

def test_manual_out_of_range():
    over = [0xF7, 0xBF, 0xBF, 0xBF, 0, 0]  # > U+10FFFF
    val, length, err = utf8_decode(over[:4])
    assert err or val is None

def test_sample_surrogates():
    for surr in range(0xDC00, 0xE000, 33):
        buf = []
        n = utf8_encode(buf, surr)
        if n == 0:
            continue
        val, length, err = utf8_decode(buf)
        assert err

def test_noncanonical_cases():
    bad1 = [0xC1, 0x82, 0]
    val, length, err = utf8_decode(bad1[:2])
    assert err

    bad2 = [0xE0, 0x81, 0xAD, 0]
    val, length, err = utf8_decode(bad2[:3])
    assert err

    bad3 = [0xF0, 0x80, 0x91, 0x8b, 0]
    val, length, err = utf8_decode(bad3[:4])
    assert err

def test_overlong_nuls():
    nul2 = [0xC0, 0x80, 0]
    nul3 = [0xE0, 0x80, 0x80, 0]
    nul4 = [0xF0, 0x80, 0x80, 0x80, 0]

    val2, length2, err2 = utf8_decode(nul2[:2])
    val3, length3, err3 = utf8_decode(nul3[:3])
    val4, length4, err4 = utf8_decode(nul4[:4])

    assert err2 and err3 and err4

def test_spot_decode():
    yen = [0xC2, 0xA5, 0]
    val, length, err = utf8_decode(yen[:2])
    assert val == 0x00A5 and length == 2 and not err

    lambda_ = [0xCE, 0xBB]
    val, length, err = utf8_decode(lambda_[:2])
    assert val == 0x03BB and length == 2 and not err

    bicycle = [0xF0, 0x9F, 0x9A, 0xB2]
    val, length, err = utf8_decode(bicycle[:4])
    assert val == 0x1F6B2 and length == 4 and not err

    pi = [0xCF, 0x80]
    val, length, err = utf8_decode(pi[:2])
    assert val == 0x03C0 and length == 2 and not err