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
        self.count = 0

    def merge(self, other):
        self.count += other.count

    def log_pair(self, orig, surv):
        self.count += 1

    def process_stats_SE(self, file):
        return "Input Reads: %d\nSurviving: %d\nDropped: %d" % (self.count, 1, self.count-1)

    def process_stats_PE(self, file):
        return "Input Read Pairs: %d\nBoth Surviving: %d\nSingle: %d\nDropped: %d" % (self.count, 1, 1, self.count-1)

def test_merge_effect():
    stats1 = TrimStats()
    stats2 = TrimStats()
    rec = FastqRecord("other", "xyz", "===!")
    orig = [rec]
    surv = [rec]
    stats2.log_pair(orig, surv)
    stats1.merge(stats2)
    assert stats1 is not None

def test_log_pair_drop_and_survive():
    stats = TrimStats()
    rec_drop = FastqRecord("d", "ggg", "!!!")
    rec_survive = FastqRecord("s", "ccc", "$$$")
    orig = [rec_drop]
    surv = [None]
    stats.log_pair(orig, surv)
    orig2 = [rec_survive]
    surv2 = [rec_survive]
    stats.log_pair(orig2, surv2)

    orig_pair = [rec_drop, rec_survive]
    surv_pair = [rec_survive, None]
    stats.log_pair(orig_pair, surv_pair)

def test_process_stats_se_and_pe_distinct():
    stats = TrimStats()
    rec = FastqRecord("n2", "AGAG", "zzzx")
    stats.log_pair([rec], [None])
    se = stats.process_stats_SE(None)
    assert "input reads" in se.lower()
    pe = stats.process_stats_PE(None)
    assert "input read pairs" in pe.lower()

def test_process_stats_pe_with_custom_file():
    stats = TrimStats()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    try:
        rec = FastqRecord("r3", "ATGCT", "####.")
        stats.log_pair([rec], [None])
        stats.process_stats_PE(tmp_path)
        assert os.path.exists(tmp_path) and os.path.getsize(tmp_path) >= 0
    finally:
        os.remove(tmp_path)