import cemu.errors

def test_assembly_exception():
    e = cemu.errors.AssemblyException("msg")
    assert isinstance(e, Exception)
    assert str(e) == "msg"