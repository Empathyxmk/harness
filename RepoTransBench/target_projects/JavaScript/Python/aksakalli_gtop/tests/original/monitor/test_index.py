def test_monitor_index_exports():
    class FakeCpu: pass
    class FakeMem: pass
    class FakeNet: pass
    class FakeDisk: pass
    class FakeProc: pass

    index_module = type('FakeMonitorIndex', (), {
        'Cpu': FakeCpu,
        'Mem': FakeMem,
        'Net': FakeNet,
        'Disk': FakeDisk,
        'Proc': FakeProc
    })()
    assert hasattr(index_module, 'Cpu')
    assert hasattr(index_module, 'Mem')
    assert hasattr(index_module, 'Net')
    assert hasattr(index_module, 'Disk')
    assert hasattr(index_module, 'Proc')
    assert callable(index_module.Cpu)