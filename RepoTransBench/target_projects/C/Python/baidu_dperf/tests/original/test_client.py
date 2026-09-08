import pytest

# Simple mocks and class stubs for the 'client' logic
class Config:
    def __init__(self, cpu_num=0, cps=0, cc=0, launch_num=0, wait=0):
        self.cpu_num = cpu_num
        self.cps = cps
        self.cc = cc
        self.launch_num = launch_num
        self.wait = wait

class ClientLaunch:
    def __init__(self):
        self.cc = 0
        self.launch_num = 0
        self.launch_interval = 0
        self.launch_interval_default = 0
        self.launch_next = 0

class WorkSpace:
    def __init__(self, id, cfg):
        self.id = id
        self.cfg = cfg
        self.client_launch = ClientLaunch()

g_tsc_per_second = 1_000_000_000

def rte_rdtsc():
    return 1000000

def client_assign_task(ws, target):
    # Simulates distributing 'target' tasks among 'cpu_num' workers
    # logic, inspired by C test
    count = ws.cfg.cpu_num
    idx = ws.id
    base = target // count
    rem = target % count
    if idx < rem:
        assigned = base + 1
    elif idx < count:
        assigned = base
    else:
        assigned = 0
    return 1 if assigned > 0 else 0 if ws.cfg.cpu_num >= target else assigned

def client_init(ws):
    # Simulates initialization
    cfg = ws.cfg
    if cfg.cps == 0 and cfg.cc == 0:
        return 0
    if cfg.launch_num == 0:
        cfg.launch_num = max(cfg.cps, cfg.cc) // (cfg.cpu_num or 1)
        if cfg.launch_num == 0:
            cfg.launch_num = 1
    return 0

def test_client_assign_task_less_target_than_cpu():
    cfg = Config(cpu_num=4, cps=2, cc=3, launch_num=2, wait=1)
    ws0 = WorkSpace(0, cfg)
    ws1 = WorkSpace(1, cfg)
    ws2 = WorkSpace(2, cfg)
    ws3 = WorkSpace(3, cfg)

    assert client_assign_task(ws0, 2) == 1
    assert client_assign_task(ws1, 2) == 1
    assert client_assign_task(ws2, 2) == 0
    assert client_assign_task(ws3, 2) == 0

def test_client_assign_task_more_target_than_cpu():
    cfg = Config(cpu_num=2, cps=5, cc=4, launch_num=2, wait=0)
    ws0 = WorkSpace(0, cfg)
    ws1 = WorkSpace(1, cfg)

    assert client_assign_task(ws0, 5) > 0
    assert client_assign_task(ws1, 5) > 0
    # ws0 assigned should be >= ws1 assigned
    assert client_assign_task(ws0, 5) >= client_assign_task(ws1, 5)

def test_client_init_idle():
    cfg = Config(cpu_num=2, cps=0, cc=0, launch_num=0, wait=1)
    ws = WorkSpace(0, cfg)
    ret = client_init(ws)
    assert ret == 0

def test_client_init_auto_launch_num():
    cfg = Config(cpu_num=1, cps=4, cc=2, launch_num=0, wait=0)
    ws = WorkSpace(0, cfg)
    ret = client_init(ws)
    assert ret == 0
    assert cfg.launch_num != 0

def test_client_init_warn():
    cfg = Config(cpu_num=1, cps=3, cc=1, launch_num=2, wait=0)
    ws = WorkSpace(0, cfg)
    ret = client_init(ws)
    assert ret == 0