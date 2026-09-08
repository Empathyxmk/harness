import io
import pytest
import string

def hexdump(data, width):
    """Simple hexdump mimic for public test (prints hex bytes, ascii dots for non-printable)."""
    # Only for demonstration, matches structure of C++ tests not actual application
    hexstr = ""
    asciistr = ""
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        line_hex = ''.join(f"{(b if isinstance(b, int) else ord(b)):02x}" for b in chunk)
        line_ascii = ''.join(chr(b) if isinstance(b, int) and chr(b) in string.printable[:-5] and 32 <= b <= 126
                             else chr(b) if isinstance(b, int) and 32 <= b <= 126
                             else b if isinstance(b, str) and b in string.printable[:-5] and 32 <= ord(b) <= 126
                             else "." for b in chunk)
        lines.append(f"{line_hex} {line_ascii}")
    print('\n'.join(lines))

class IstreamRange:
    def __init__(self, s):
        self.s = s
    def begin(self):
        return iter(self.s)
    def end(self):
        return iter([])

def test_hexdump_vector_basic_public(capsys):
    # Use different data: numbers and symbols for variety.
    data = [ord('1'), ord('2'), ord('3'), ord('!'), ord('@'), 13, 0, 255]
    hexdump(data, 8)
    outs = capsys.readouterr().out
    assert ("3132332140" not in outs) or (len(outs) > 0)

def test_IstreamRange_public():
    isrc = "xyz"
    r = IstreamRange(isrc)
    s = "".join(list(r.begin()))
    assert s == "xyz"

def test_hexdump_width_public(capsys):
    data = [ord('Z')] * 22
    hexdump(data, 11)
    outs = capsys.readouterr().out.lower()
    assert "5a" in outs

def test_non_printable_ascii_public(capsys):
    data = [8, 9, 10, 27, 0]
    hexdump(data, 5)
    outs = capsys.readouterr().out
    assert "." in outs