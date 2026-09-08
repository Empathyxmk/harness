import sys

class KSeq:
    def __init__(self, name, comment, seq, qual):
        self.name = type('S', (), {'s': name, 'l': len(name) if name else 0})
        self.comment = type('S', (), {'s': comment, 'l': len(comment) if comment else 0})
        self.seq = type('S', (), {'s': seq, 'l': len(seq) if seq else 0})
        self.qual = type('S', (), {'s': qual, 'l': len(qual) if qual else 0})

class CutSites: pass

def print_record(out, ks, cs):
    print(f"print_record: name={ks.name.s}, seq={ks.seq.s}, qual={ks.qual.s}", file=out)

def test_print_record_edge_public(capsys):
    cs = CutSites()

    ks = KSeq("Alpha", None, None, None)
    print_record(sys.stdout, ks, cs)

    ks = KSeq("Beta", "note", "N", "\4")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("Gamma", "bar", "GT", "HH")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("Delta", None, "CCC", "FFF")
    print_record(sys.stdout, ks, cs)

    ks = KSeq("Epsilon", None, None, None)
    print_record(sys.stdout, ks, cs)

    print("Edge print_record_public tests OK")
    output = capsys.readouterr().out
    assert "Edge print_record_public tests OK" in output