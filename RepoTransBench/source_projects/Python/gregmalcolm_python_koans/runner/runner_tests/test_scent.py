import os
import sys
import types

def test_py_files_validator():
    import scent
    assert scent.py_files('abc.py')
    assert not scent.py_files('.abc.py')
    assert not scent.py_files('abc.txt')

def test_execute_koans_runs(monkeypatch):
    import scent
    result = {}
    def fake_system(cmd):
        result['cmd'] = cmd
        return 0
    monkeypatch.setattr(os, 'system', fake_system)
    scent.execute_koans()
    assert result['cmd'].endswith('contemplate_koans.py')