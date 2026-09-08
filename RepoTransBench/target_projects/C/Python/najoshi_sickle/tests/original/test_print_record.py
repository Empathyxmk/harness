import sys

class KSeq:
    def __init__(self, name, comment, seq, qual):
        self.name = type("S", (), {"s": name, "l": len(name)})
        self.comment = type("S", (), {"s": comment, "l": len(comment)})
        self.seq = type("S", (), {"s": seq, "l": len(seq)})
        self.qual = type("S", (), {"s": qual, "l": len(qual)})

class CutSites:
    def __init__(self, five_prime_cut, three_prime_cut):
        self.five_prime_cut = five_prime_cut
        self.three_prime_cut = three_prime_cut

def print_record(out, ks, cs):
    print(f"print_record: {ks.name.s}, {ks.comment.s}, {ks.seq.s}, {ks.qual.s}, cuts={cs.five_prime_cut},{cs.three_prime_cut}", file=out)

def print_record_N(out, ks, qualtype):
    print(f"print_record_N: {ks.name.s}, {ks.comment.s}, {ks.seq.s}, {ks.qual.s}, qualtype={qualtype}", file=out)

SANGER = 0

def test_print_record_scenario(capsys):
    seq = "ACGTAAA"
    qual = "IIIIIII"
    name = "foo"
    comment = "my comment"
    ks = KSeq(name, comment, seq, qual)
    cs = CutSites(0, 7)
    print("Testing print_record")
    print_record(sys.stdout, ks, cs)
    print_record_N(sys.stdout, ks, SANGER)
    print("All print_record tests OK")
    output = capsys.readouterr().out
    assert "All print_record tests OK" in output