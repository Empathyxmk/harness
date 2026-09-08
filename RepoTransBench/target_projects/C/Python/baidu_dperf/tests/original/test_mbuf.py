import pytest
import io

# Mocks for DPDK/net structs
class RteMempool:
    def __init__(self):
        self.created = False
        self.name = ""

class RteMbuf:
    def __init__(self):
        self.dummy = 0

class EthHdr:
    def __init__(self):
        self.type = 0

class Iphdr:
    def __init__(self):
        self.protocol = 0

class Tcphdr:
    def __init__(self):
        self.th_flags = 0

class Ip6Hdr:
    def __init__(self):
        self.dummy = [0]*40

class WorkSpace:
    def __init__(self):
        self.log = None

class MbufData:
    def __init__(self):
        self.data = bytearray(60)

class Config:
    def __init__(self):
        self.jumbo = 0

g_config = Config()
space = WorkSpace()
g_work_space = space
g_current_seconds = 0
g_current_ticks = 0

def eth_addr_to_str(addr, out):
    return "00:00:00:00:00:00"

def mbuf_eth_hdr(m):
    return EthHdr()

def mbuf_ip_hdr(m):
    return Iphdr()

def mbuf_tcp_hdr(m):
    return Tcphdr()

def mbuf_ip6_hdr(m):
    return Ip6Hdr()

def mbuf_pool_create(name, a, b):
    # Returns None to simulate lack of rte_pktmbuf_pool_create
    return None

def mbuf_log(m, msg):
    # Writes a log to file if log exists, else passes
    if hasattr(g_work_space, "log") and g_work_space.log is not None:
        print(f"{msg}", file=g_work_space.log)

def test_mbuf_pool_create():
    mp = mbuf_pool_create("mbuf", 0, 0)
    assert mp is None

def test_mbuf_log_runs(tmp_path):
    m = RteMbuf()
    null_fp = (tmp_path / "dummy.log").open("w")
    g_work_space.log = null_fp
    mbuf_log(m, "test")
    null_fp.close()