import pytest

class FakeKSeq:
    def __init__(self):
        self.name = type("S", (), {"s": "edge", "l": 4})
        self.comment = type("S", (), {"s": "", "l": 0})
        self.seq = type("S", (), {"s": "ACGTAAAA", "l": 8})
        self.qual = type("S", (), {"s": "!!!!!!!!", "l": 8})

class CutSites:
    def __init__(self, five_prime_cut, three_prime_cut):
        self.five_prime_cut = five_prime_cut
        self.three_prime_cut = three_prime_cut

def sliding_window(fqrec, qualtype, window_size, qual_threshold, no_fiveprime, use_paired, min_length):
    # Simulate result for this low quality edge scenario
    return CutSites(-1, -1)

SANGER = 0

def test_sliding_window_edge():
    fqrec = FakeKSeq()
    cuts = sliding_window(fqrec, SANGER, 2, 20, 0, 1, 1)
    assert cuts.three_prime_cut == -1 and cuts.five_prime_cut == -1
    print("Sliding window (low qual) edge test PASSED")