import os
import sys
import pytest

from Chapter11 import window_command

def test_document_save(tmp_path):
    filename = tmp_path / "file1.txt"
    doc = window_command.Document(str(filename))
    doc.save()
    assert filename.read_text() == "This file cannot be modified"

def test_save_command_executes_document_save(tmp_path):
    filename = tmp_path / "file2.txt"
    doc = window_command.Document(str(filename))
    doc.contents = "SAVED"
    cmd = window_command.SaveCommand(doc)
    cmd.execute()
    assert filename.read_text() == "SAVED"

def test_toolbarbutton_click_calls_command(monkeypatch):
    class DummyCommand:
        def execute(self): 
            self.x = True
    button = window_command.ToolbarButton("n", "icon")
    dummy = DummyCommand()
    button.command = dummy
    dummy.x = False
    button.click()
    assert dummy.x

def test_keyboardshortcut_keypress_executes_command():
    class Dummy:
        def execute(self): self.called = True
    ks = window_command.KeyboardShortcut("k","ctrl")
    dummy = Dummy()
    dummy.called = False
    ks.command = dummy
    ks.keypress()
    assert dummy.called

def test_menuitem_click_calls_command():
    class Dummy:
        def execute(self): self.did = True
    m = window_command.MenuItem("F", "X")
    dummy = Dummy()
    dummy.did = False
    m.command = dummy
    m.click()
    assert dummy.did

def test_exit_command_exits(monkeypatch):
    monkeypatch.setattr(sys, "exit", lambda x=0: (_ for _ in ()).throw(SystemExit(x)))
    w = window_command.Window()
    cmd = window_command.ExitCommand(w)
    with pytest.raises(SystemExit) as e:
        cmd.execute()
    assert e.value.code == 0