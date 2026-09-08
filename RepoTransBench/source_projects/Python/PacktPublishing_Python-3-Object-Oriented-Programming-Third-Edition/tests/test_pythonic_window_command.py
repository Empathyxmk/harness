import pytest
import os
import sys

from Chapter11 import pythonic_window_command

def test_document_save(tmp_path):
    filename = tmp_path / "doc.txt"
    doc = pythonic_window_command.Document(str(filename))
    doc.save()
    assert filename.read_text() == "This file cannot be modified"

def test_save_command_calls_document_save(tmp_path):
    filename = tmp_path / "doc.txt"
    doc = pythonic_window_command.Document(str(filename))
    called = []
    orig_save = doc.save
    doc.save = lambda : called.append(True) or orig_save()
    cmd = pythonic_window_command.SaveCommand(doc)
    cmd()
    assert called

def test_keyboard_shortcut_calls_command(monkeypatch):
    class DummyCommand:
        def __call__(self):
            self.called = True
    cmd = DummyCommand()
    ks = pythonic_window_command.KeyboardShortcut()
    ks.command = cmd
    cmd.called = False
    ks.keypress()
    assert cmd.called is True

def test_menuitem_click_calls_command(monkeypatch):
    class D:
        def __call__(self): self.called = True
    dummy = D()
    dummy.called = False
    item = pythonic_window_command.MenuItem()
    item.command = dummy
    item.click()
    assert dummy.called

def test_window_exit_exits(monkeypatch):
    monkeypatch.setattr(sys, "exit", lambda x=0: (_ for _ in ()).throw(SystemExit(x)))
    w = pythonic_window_command.Window()
    with pytest.raises(SystemExit) as e:
        w.exit()
    assert e.value.code == 0