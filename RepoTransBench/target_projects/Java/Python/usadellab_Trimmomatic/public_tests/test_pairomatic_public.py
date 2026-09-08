import pytest
import tempfile
import os
from collections import OrderedDict

class DummyPublicFastqRecord:
    def __init__(self, n):
        self.name = n
        self.seq = "TGCA"
        self.qual = "@@@@"

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

def create_temp_fastq(names, delimiter):
    fd, path = tempfile.mkstemp(suffix=".fastq", prefix="pairo_pub")
    with os.fdopen(fd, "w") as w:
        for n in names:
            full_name = f"{n}{delimiter}2" if delimiter else n
            w.write(f"@{full_name}\n")
            w.write("TGCA\n+\n@@@@\n")
    return path

def test_get_fastq_names_delimiter_dash():
    p = Pairomatic()
    names = ["QX", "ZE"]
    f = create_temp_fastq(names, '-')
    try:
        result = p.get_fastq_names(f, '-')
        assert len(result) == 2
    finally:
        os.remove(f)

def test_get_fastq_names_no_delimiter_multiple():
    p = Pairomatic()
    names = ["A010", "B020"]
    f = create_temp_fastq(names, None)
    try:
        result = p.get_fastq_names(f, None)
        assert len(result) == 2
    finally:
        os.remove(f)

def test_get_fastq_names_fail_on_delimiter():
    p = Pairomatic()
    names = ["NM"]
    f = create_temp_fastq(names, None)
    try:
        with pytest.raises(RuntimeError) as ex:
            p.get_fastq_names(f, '-')
        assert "Failed to find expected delimiter" in str(ex.value)
    finally:
        os.remove(f)

def test_equal_ordering_mismatch():
    p = Pairomatic()
    s1 = OrderedDict([("U", True), ("V", True)])
    s2 = OrderedDict([("V", True), ("U", True)])
    assert not p.equal_ordering(s1, s2)
    s3 = OrderedDict([("U", True), ("V", True)])
    assert p.equal_ordering(s1, s3)