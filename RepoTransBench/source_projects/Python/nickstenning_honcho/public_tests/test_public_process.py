from honcho.process import Process

def test_public_process_init():
    p = Process("worker.3", "proc_cmd", env={"HELLO": "world"})
    assert p.name == "worker.3"
    assert p.cmd == "proc_cmd"
    assert p.env["HELLO"] == "world"