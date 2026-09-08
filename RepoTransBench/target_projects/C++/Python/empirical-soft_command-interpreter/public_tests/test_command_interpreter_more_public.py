import pytest
from src.command_interpreter import CommandInterpreter
import io

def run_command_and_capture(ci, cmd):
    out = io.StringIO()
    ci.execute(cmd, out)
    return out.getvalue()

def register_commands(ci):
    ci.add_command("add2", lambda i, o: (lambda x, y: o.write(f"{int(x)+int(y)}\n"))(*i.read().split()), "Add two numbers")
    ci.add_command("sub2", lambda i, o: (lambda x, y: o.write(f"{int(x)-int(y)}\n"))(*i.read().split()), "Subtract two numbers")
    ci.add_command("reverse", lambda i, o: (lambda s: o.write(f"{s[::-1]}\n"))(*i.read().split()), "Reverse a string")

def test_public_more_ci_all():
    ci = CommandInterpreter()
    register_commands(ci)
    # add2
    assert run_command_and_capture(ci, "add2 100 200") == "300\n"
    assert run_command_and_capture(ci, "add2 -5 10") == "5\n"
    # sub2
    assert run_command_and_capture(ci, "sub2 88 44") == "44\n"
    assert run_command_and_capture(ci, "sub2 5 7") == "-2\n"
    # reverse
    assert run_command_and_capture(ci, "reverse dog") == "god\n"
    assert run_command_and_capture(ci, "reverse Madam") == "madaM\n"

    # help output
    got = run_command_and_capture(ci, "help")
    expected = (
        "add2    Add two numbers\n"
        "sub2    Subtract two numbers\n"
        "reverse Reverse a string\n"
        "help    Show this help\n"
    )
    def norm(s):
        out, in_space = '', False
        for c in s:
            if c.isspace():
                if not in_space:
                    out += ' '
                in_space = True
            else:
                out += c
                in_space = False
        return out.strip()
    assert norm(got) == norm(expected)

    assert run_command_and_capture(ci, "foo 321") == "Unknown command: foo\n"
    assert run_command_and_capture(ci, "") == ""