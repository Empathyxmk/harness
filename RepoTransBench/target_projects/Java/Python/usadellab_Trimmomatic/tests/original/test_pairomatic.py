import pytest
import tempfile
import os
from collections import OrderedDict

class DummyFastqRecord:
    def __init__(self, n):
        self.name = n
        self.seq = "ACGT"
        self.qual = "!!!"

class Pairomatic:
    def get_fastq_names(self, filepath, delimiter):
        names = OrderedDict()
        with open(filepath, "r") as f:
            lines = f.readlines()
            for i in range(0, len(lines), 4):
                header = lines[i].strip()
                if not header.startswith("@"):
                    raise RuntimeError(f"Invalid FASTQ header: {header}")
                head_name = header[1:]
                if delimiter is not None:
                    if delimiter not in head_name:
                        raise RuntimeError("Failed to find expected delimiter")
                    head_name = head_name.split(delimiter, 1)[0]
                names[head_name] = True
        return names

    def equal_ordering(self, s1, s2):
        return list(s1.keys()) == list(s2.keys())

def create_fastq_file(names, delimiter):
    fd, path = tempfile.mkstemp(suffix=".fastq", prefix="pairo")
    with os.fdopen(fd, "w") as w:
        for n in names:
            full_name = f"{n}{delimiter}1" if delimiter else n
            w.write(f"@{full_name}\n")
            w.write("ACGT\n+\n!!!!\n")
    return path

def test_get_fastq_names_no_delimiter():
    p = Pairomatic()
    names = ["x1", "y2"]
    f = create_fastq_file(names, None)
    try:
        result = p.get_fastq_names(f, None)
        assert len(result) == 2
    finally:
        os.remove(f)

def test_get_fastq_names_with_delimiter():
    p = Pairomatic()
    names = ["A", "B"]
    f = create_fastq_file(names, ':')
    try:
        result = p.get_fastq_names(f, ':')
        assert len(result) == 2
    finally:
        os.remove(f)

def test_get_fastq_names_delimiter_not_found():
    p = Pairomatic()
    names = ["Z"]
    f = create_fastq_file(names, None)
    try:
        with pytest.raises(RuntimeError) as ex:
            p.get_fastq_names(f, ':')
        assert "Failed to find expected delimiter" in str(ex.value)
    finally:
        os.remove(f)

def test_equal_ordering():
    p = Pairomatic()
    s1 = OrderedDict([("A", True), ("B", True)])
    s2 = OrderedDict([("A", True), ("B", True)])
    assert p.equal_ordering(s1, s2)
    s3 = OrderedDict([("B", True), ("A", True)])
    assert not p.equal_ordering(s1, s3)