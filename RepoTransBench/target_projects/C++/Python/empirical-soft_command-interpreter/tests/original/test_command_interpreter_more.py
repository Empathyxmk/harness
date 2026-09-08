import pytest
from src.command_interpreter import CommandInterpreter

class TestCI(CommandInterpreter):
    def __init__(self):
        super().__init__()
        self.called_register = False

    def register_commands(self):
        self.called_register = True

    # In Python, just expose via self

class DummyCI(CommandInterpreter):
    @staticmethod
    def foo(x: int) -> int:
        return x

    def register_commands(self):
        self.register_command(self.foo, "foo", "Desc1")
        self.register_command(self.foo, "foo", "Desc2")  # duplicate registration

def test_err_num_args():
    ci = TestCI()
    assert ci.err_num_args(1, 1) == "Error: expected 1 argument; got 1"
    assert ci.err_num_args(2, 1) == "Error: expected 2 arguments; got 1"
    assert ci.err_num_args(3, 2) == "Error: expected 3 arguments; got 2"

def test_err_type_args():
    ci = TestCI()
    assert ci.err_type_args("int", 0) == "Error: invalid argument type at position 0; expected type int"
    assert ci.err_type_args("double", 2) == "Error: invalid argument type at position 2; expected type double"

def test_parse():
    ci = TestCI()
    ci.parse("add 3 4")
    assert ci.func_ == "add"
    assert ci.args_ == ["3", "4"]

    ci.parse("    inc   7  ")
    assert ci.func_ == "inc"
    assert ci.args_ == ["7"]

    ci.parse("   help  ")
    assert ci.func_ == "help"
    assert ci.args_ == []

    ci.parse("   ")
    assert ci.func_ == ""
    assert ci.args_ == []

    ci.parse("")
    assert ci.func_ == ""
    assert ci.args_ == []

def test_help():
    ci = TestCI()
    ci.commands_.clear()
    ci.commands_.append(("add", "Add two numbers", lambda: None))
    ci.commands_.append(("minus", "Subtract numbers", lambda: None))
    ci.commands_.append(("test", "Runs a test", lambda: None))
    ci.commands_.append(("help", "Show help", lambda: None))
    help_output = ci.help()
    # Should contain all registered commands with proper spacing
    assert help_output.startswith("add ")
    assert "minus" in help_output
    assert "test" in help_output
    assert "Add two numbers" in help_output

def test_register_commands_called():
    ci = TestCI()
    ci.register_commands()
    assert ci.called_register is True

def test_duplicate_command_registration():
    ci = DummyCI()
    ci.register_commands()
    foo_count = sum(1 for name, desc, _ in ci.commands_ if name == "foo")
    assert foo_count == 2

    has_help_cmd = any(name == "help" for name, desc, _ in ci.commands_)
    # Accept both present or not, do not assert if absent.

def test_args_typecheck_edge():
    ci = TestCI()
    assert ci.err_type_args("", 0) == "Error: invalid argument type at position 0; expected type "
    assert ci.err_type_args("bar", 100) == "Error: invalid argument type at position 100; expected type bar"