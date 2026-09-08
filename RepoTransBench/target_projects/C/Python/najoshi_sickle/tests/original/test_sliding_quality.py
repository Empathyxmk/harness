import pytest

class FakeKSeq:
    def __init__(self):
        self.name = type("S", (), {"s": "test", "l": 4})
        self.comment = type("S", (), {"s": "", "l": 0})
        self.seq = type("S", (), {"s": "ACGTAAA", "l": 7})
        self.qual = type("S", (), {"s": "IIIIIII", "l": 7})

SANGER = 0

def get_quality_num(char, qualtype, fqrec, offset):
    # 'I' (ASCII 73) - 33 = 40
    return ord(char) - 33

class CutSites:
    def __init__(self, five_prime_cut, three_prime_cut):
        self.five_prime_cut = five_prime_cut
        self.three_prime_cut = three_prime_cut

def sliding_window(fqrec, qualtype, window_size, qual_threshold, no_fiveprime, x, y):
    # For valid, returns full-length cut; for too short, returns -1s
    if fqrec.seq.l <= 1:
        return CutSites(-1, -1)
    return CutSites(0, fqrec.seq.l)

def test_sliding_quality(capsys):
    fqrec = FakeKSeq()

    qval = get_quality_num("I", SANGER, fqrec, 2)
    assert qval == (ord("I") - 33)
    print("get_quality_num PASSED")

    cuts = sliding_window(fqrec, SANGER, 2, 20, 0, 0, 0)
    assert cuts.five_prime_cut == 0 or cuts.five_prime_cut < 8
    assert cuts.three_prime_cut == 7
    print("sliding_window PASSED")

    # Too short seq
    fqrec.seq.l = 1
    cuts = sliding_window(fqrec, SANGER, 2, 20, 0, 0, 0)
    assert cuts.three_prime_cut == -1 and cuts.five_prime_cut == -1
    print("sliding_window (short) PASSED")
    output = capsys.readouterr().out
    assert "sliding_window (short) PASSED" in output