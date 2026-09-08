import pytest

class Command:
    def __init__(self, name, args):
        self._name = name
        self._args = list(args)
    def name(self):
        return self._name
    def args(self):
        return list(self._args)
    def __eq__(self, other):
        if not isinstance(other, Command):
            return False
        return self._name == other._name and list(self._args) == list(other._args)

def test_parse_new_command_name():
    cmd = Command("update", ["arg1", "arg2"])
    assert cmd.name() == "update"
    assert len(cmd.args()) == 2
    assert cmd.args()[0] == "arg1"
    assert cmd.args()[1] == "arg2"

def test_handles_whitespace_in_args():
    cmd = Command("copy", ["file 1.txt", "dir 2"])
    assert len(cmd.args()) == 2
    assert cmd.args()[0] == "file 1.txt"
    assert cmd.args()[1] == "dir 2"

def test_empty_args_allowed():
    cmd = Command("exit", [])
    assert cmd.name() == "exit"
    assert len(cmd.args()) == 0

def test_eq_operator_different_commands():
    cmd1 = Command("diff", ["fileA", "fileB"])
    cmd2 = Command("diff", ["fileA", "fileB"])
    cmd3 = Command("diff", ["fileC", "fileD"])
    assert cmd1 == cmd2
    assert cmd1 != cmd3

def test_not_eq_when_name_differs():
    cmd1 = Command("start", ["process1"])
    cmd2 = Command("stop", ["process1"])
    assert not (cmd1 == cmd2)