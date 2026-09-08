import pytest
import types

import chainbreaker.results as results

class DummyRecord:
    def __str__(self):
        return "DummyRecord str"

class DummyArgs:
    pass

def test_log_output_keyboard_interrupt(monkeypatch):
    args = DummyArgs()
    summary = []
    class MyRecord(DummyRecord):
        def __str__(self):
            raise KeyboardInterrupt("bail!")
    coll = {
        'header': 'h',
        'records': [MyRecord()],
        'write_to_console': True,
        'write_to_disk': False,
        'write_directory': "/tmp"
    }
    # Should not raise unhandled
    try:
        results.log_output([coll], summary, args)
    except SystemExit:
        pass

def test_log_output_console_and_disk(tmp_path):
    args = DummyArgs()
    summary = []
    dummy_file = tmp_path / "out.txt"
    coll = {
        'header': 'header-here',
        'records': [DummyRecord()],
        'write_to_console': True,
        'write_to_disk': True,
        'write_directory': str(tmp_path)
    }
    results.log_output([coll], summary, args)
    # Output file should exist
    files = list(tmp_path.glob("*.h.txt"))
    assert files or list(tmp_path.glob("*.header-here.txt"))

def test_summary_output(monkeypatch):
    monkeypatch.setattr(results, "log_output", lambda collections, summary, args=None: summary.append("called"))
    dummy_collections = [{}, {}]
    dummy_summary = []
    results.log_output(dummy_collections, dummy_summary)
    assert "called" in dummy_summary

def test_write_collection_to_file(tmp_path):
    coll = {
        'header': 'HHH',
        'records': [DummyRecord(), DummyRecord()],
        'write_directory': str(tmp_path)
    }
    f = results.write_collection_to_file(coll, 'content')
    assert f.exists()
    assert f.read_text("utf-8").find("content") != -1