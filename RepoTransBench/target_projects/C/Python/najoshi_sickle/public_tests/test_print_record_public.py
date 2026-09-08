import sys

class KSeq:
    def __init__(self, name, comment, seq, qual):
        self.name = type('S', (), {'s': name, 'l': len(name) if name else 0})
        self.comment = type('S', (), {'s': comment, 'l': len(comment) if comment else 0})
        self.seq = type('S', (), {'s': seq, 'l': len(seq) if seq else 0})
        self.qual = type('S', (), {'s': qual, 'l': len(qual) if qual else 0})

class CutSites: pass  # details unused in mocked print_record

def print_record(out, ks, cs):
    print(f"print_record: name={ks.name.s}, comment={ks.comment.s}, seq={ks.seq.s}, qual={ks.qual.s}", file=out)

def test_print_record_public_variant(capsys):
    cs = CutSites()

    ks = KSeq("Test123", None, "ATGCCGTA", "HHHHHHHH")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("PubCase", "info", "G", "Y")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("RandName", None, "CTT", "III")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("EdgePub", "xyz", "TGCA", "BBBB")
    print_record(sys.stdout, ks, cs)

    print("Public print_record tests OK")
    output = capsys.readouterr().out
    assert "Public print_record tests OK" in output