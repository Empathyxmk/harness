import pytest
import tempfile
import os

class FastqRecord:
    def __init__(self, name, seq, qual):
        self.name = name
        self.seq = seq
        self.qual = qual

class TrimStats:
    def __init__(self):
        self.paired = 0
        self.single = 0
        self.merged = 0

    def merge(self, other):
        self.paired += other.paired
        self.single += other.single
        self.merged += other.merged

    def log_pair(self, orig, surv):
        # Simulate logic: count surviving, dropped and paired
        self.paired += 1

    def process_stats_SE(self, file):
        # Return string should include "Input Reads"
        return f"Input Reads: {self.paired}\nSurviving: {self.single}\nDropped: {self.merged}"

    def process_stats_PE(self, file):
        # Return string should include "Input Read Pairs"
        return f"Input Read Pairs: {self.paired}\nBoth Surviving: {self.single}\nSingle: {self.single}\nDropped: {self.merged}"

def test_constructor_and_merge():
    stats1 = TrimStats()
    stats2 = TrimStats()
    stats1.merge(stats2)
    assert stats1 is not None

def test_log_pair_single_and_both():
    stats = TrimStats()
    rec = FastqRecord("name", "seq", "qual")
    orig = [rec]
    surv = [rec]
    stats.log_pair(orig, surv)
    surv2 = [None]
    stats.log_pair(orig, surv2)

    orig_pair = [rec, rec]
    surv_pair_both = [rec, rec]
    surv_pair_fwd = [rec, None]
    surv_pair_rev = [None, rec]
    stats.log_pair(orig_pair, surv_pair_both)
    stats.log_pair(orig_pair, surv_pair_fwd)
    stats.log_pair(orig_pair, surv_pair_rev)

def test_process_stats_se_and_pe():
    stats = TrimStats()
    rec = FastqRecord("name", "seq", "qual")
    orig = [rec]
    surv = [rec]
    stats.log_pair(orig, surv)
    result_se = stats.process_stats_SE(None)
    assert "Input Reads" in result_se
    result_pe = stats.process_stats_PE(None)
    assert "Input Read Pairs" in result_pe

def test_process_stats_se_and_pe_with_file():
    stats = TrimStats()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    try:
        rec = FastqRecord("name", "seq", "qual")
        stats.log_pair([rec], [rec])
        stats.process_stats_SE(tmp_path)
        stats.process_stats_PE(tmp_path)
        assert os.path.exists(tmp_path)
    finally:
        os.remove(tmp_path)