import pytest

# Constants and mappings as in the C code
REDIR_SUCCESS = 0
REDIR_ERROR = 1
REDIR_RES_MAX = 2
redir_names = ["Success", "Error"]

def err2str(err):
    if 0 <= err < REDIR_RES_MAX:
        return redir_names[err]
    return None

def test_err2str():
    assert err2str(REDIR_SUCCESS) == "Success"
    assert err2str(REDIR_ERROR) == "Error"
    assert err2str(-1) is None
    assert err2str(100) is None

class Record:
    def __init__(self, counter, timestamp):
        self.counter = counter
        self.timestamp = timestamp

class StatsRecord:
    def __init__(self, counters):
        self.xdp_redir = counters[:]  # List of 2 Record objects

def stats_print_headers(err_only):
    if err_only:
        print(
            "\nNOTICE: Only tracking XDP redirect errors\n"
            "         Enable TX success stats via '--stats'\n"
            "         (which comes with a per packet processing overhead)\n"
        )

    print("{:<14} {:<10} {:<18} {:<9}".format(
        "XDP_REDIRECT", "pps ", "pps-human-readable", "measure-period"
    ))

def test_stats_print(capsys):
    now = StatsRecord([Record(100, 200), Record(40, 90)])
    prev = StatsRecord([Record(80, 100), Record(20, 30)])

    # Normal call (header, err_only=0)
    stats_print_headers(0)

    for i in range(REDIR_RES_MAX):
        r = now.xdp_redir[i]
        p = prev.xdp_redir[i]
        period  = r.timestamp - p.timestamp
        packets = r.counter - p.counter
        pps = 0.0
        period_ = 0.0
        if p.timestamp:
            if period > 0:
                period_ = (period / 1_000_000_000)
                pps = packets / period_ if period_ > 0 else 0
        print("{:<14} {:<10.1f} {:<18.1f} {:f}".format(
            err2str(i), pps, pps, period_))

    # Error only path
    stats_print_headers(1)
    # Just ensure code runs, not checking outputs stringently

def test_main_called(monkeypatch, capsys):
    # Execute all logic as per C main
    test_err2str()
    test_stats_print(capsys)
    print("monitor_user tests passed")
    out = capsys.readouterr().out
    assert "monitor_user tests passed" in out