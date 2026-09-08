import pytest

# Replicate test logic from public C test for client (with different values)

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

g_tsc_per_second = 2_000_000_000

def rte_rdtsc():
    return 2_000_000

def client_assign_task(ws, target):
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
    cfg = ws.cfg
    if cfg.cps == 0 and cfg.cc == 0:
        return 0
    if cfg.launch_num == 0:
        cfg.launch_num = max(cfg.cps, cfg.cc) // (cfg.cpu_num or 1)
        if cfg.launch_num == 0:
            cfg.launch_num = 1
    return 0

def test_client_assign_task_less_target_than_cpu_public():
    cfg = Config(cpu_num=6, cps=3, cc=5, launch_num=3, wait=2)
    ws = [WorkSpace(i, cfg) for i in range(6)]
    # Only ws0-2 get task
    assert client_assign_task(ws[0], 3) == 1
    assert client_assign_task(ws[1], 3) == 1
    assert client_assign_task(ws[2], 3) == 1
    assert client_assign_task(ws[3], 3) == 0
    assert client_assign_task(ws[4], 3) == 0
    assert client_assign_task(ws[5], 3) == 0

def test_client_assign_task_more_target_than_cpu_public():
    cfg = Config(cpu_num=3, cps=10, cc=9, launch_num=5, wait=1)
    ws = [WorkSpace(i, cfg) for i in range(3)]
    assert client_assign_task(ws[0], 10) > 0
    assert client_assign_task(ws[1], 10) > 0
    assert client_assign_task(ws[2], 10) > 0
    # ws[0] gets the most
    assert client_assign_task(ws[0], 10) > client_assign_task(ws[1], 10)

def test_client_init_idle_public():
    cfg = Config(cpu_num=2, cps=0, cc=0, launch_num=1, wait=2)
    ws = WorkSpace(1, cfg)
    ret = client_init(ws)
    assert ret == 0

def test_client_init_auto_launch_num_public():
    cfg = Config(cpu_num=2, cps=6, cc=2, launch_num=0, wait=3)
    ws = WorkSpace(1, cfg)
    ret = client_init(ws)
    assert ret == 0
    assert cfg.launch_num != 0

def test_client_init_warn_public():
    cfg = Config(cpu_num=2, cps=5, cc=3, launch_num=3, wait=2)
    ws = WorkSpace(0, cfg)
    ret = client_init(ws)
    assert ret == 0