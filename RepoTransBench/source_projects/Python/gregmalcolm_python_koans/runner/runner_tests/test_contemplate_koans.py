import sys
import types

def test_python2_message(monkeypatch, capsys):
    sys_version_info = (2,7)
    monkeypatch.setattr(sys, 'version_info', sys_version_info)
    import importlib
    import contemplate_koans
    importlib.reload(contemplate_koans)
    out, err = capsys.readouterr()
    assert "Python 3 version" in out or "Try:" in out

def test_python36_warning(monkeypatch, capsys):
    # Should produce warning
    sys_version_info = (3,6)
    monkeypatch.setattr(sys, 'version_info', sys_version_info)
    import importlib
    import contemplate_koans
    importlib.reload(contemplate_koans)
    out, err = capsys.readouterr()
    assert "WARNING" in out and "Python 3.7 or greater" in out

def test_main_import(monkeypatch):
    # Should call Mountain().walk_the_path when version >= 3,7
    calls = []
    class DummyMountain:
        def walk_the_path(self, argv): calls.append(argv)
    monkeypatch.setitem(sys.modules, 'runner.mountain', types.ModuleType('runner.mountain'))
    sys.modules['runner.mountain'].Mountain = lambda : DummyMountain()
    sys_version_info = (3,7)
    monkeypatch.setattr(sys, 'version_info', sys_version_info)
    import importlib
    import contemplate_koans
    importlib.reload(contemplate_koans)
    assert calls # Means Mountain was called