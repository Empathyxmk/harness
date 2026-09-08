import pytest
from honcho.manager import Manager

def test_public_manager_add_and_get():
    mgr = Manager()
    mgr.add_process("new-proc", "echo testpublic")
    procs = mgr.processes
    assert "new-proc" in procs
    assert procs["new-proc"].command == "echo testpublic"

def test_public_manager_ensure_unique_name():
    mgr = Manager()
    mgr.add_process("foo", "cmd1")
    with pytest.raises(AssertionError):
        mgr.add_process("foo", "cmd2")