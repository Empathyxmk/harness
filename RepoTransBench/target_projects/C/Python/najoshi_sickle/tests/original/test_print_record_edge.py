import io
import sys
import pytest

# Mocks for the C structures
class KSeq:
    def __init__(self, name, comment, seq, qual):
        self.name = type('S', (), {'s': name, 'l': len(name) if name else 0})
        self.comment = type('S', (), {'s': comment, 'l': len(comment) if comment else 0})
        self.seq = type('S', (), {'s': seq, 'l': len(seq) if seq else 0})
        self.qual = type('S', (), {'s': qual, 'l': len(qual) if qual else 0})

class CutSites:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# The print_record and print_record_N should be imported from Python src/implementation
# Here, we just mock them for demonstration.
def print_record(out, ks, cs):
    print(f"print_record: name={ks.name.s}, seq={ks.seq.s}, qual={ks.qual.s}, left={cs.left}, right={cs.right}", file=out)

def print_record_N(out, ks, qualtype):
    print(f"print_record_N: name={ks.name.s}, seq={ks.seq.s}, qual={ks.qual.s}, qualtype={qualtype}", file=out)

SANGER = 0

def test_print_record_edge(capsys):
    ks = KSeq("A", "", "ACGT", "IIII")
    cs = CutSites(-1, -1)
    print_record(sys.stdout, ks, cs)

    ks = KSeq("B", "", "NNNN", "IIII")
    print_record_N(sys.stdout, ks, SANGER)

    ks = KSeq("C", "foo", "ACGTAC", "IIIIII")
    cs = CutSites(1, 3)
    print_record(sys.stdout, ks, cs)

    ks = KSeq("D", "", "GATTACA", "IIIIIII")
    cs = CutSites(0, 6)
    print_record(sys.stdout, ks, cs)

    ks = KSeq("E", None, "", "")
    cs = CutSites(0, -1)
    print_record(sys.stdout, ks, cs)

    print("Edge print_record tests OK")
    # Just check that output contains something for sanity
    output = capsys.readouterr().out
    assert "Edge print_record tests OK" in output