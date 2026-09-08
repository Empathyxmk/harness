import pytest
from src.command_interpreter import CommandInterpreter
import io

def run_command_and_capture(ci, cmd):
    out = io.StringIO()
    ci.execute(cmd, out)
    return out.getvalue()

def register_commands(ci):
    ci.add_command("mul", lambda i, o: (lambda x, y: o.write(f"{int(x)*int(y)}\n"))(*i.read().split()), "Multiply two numbers")
    ci.add_command("dec", lambda i, o: (lambda x: o.write(f"{int(x)-1}\n"))(*i.read().split()), "Decrement a number")
    ci.add_command("triple", lambda i, o: (lambda x: o.write(f"{int(x)*3}\n"))(*i.read().split()), "Triple a number")
    ci.add_command("upper", lambda i, o: (lambda s: o.write(f"{s.upper()}\n"))(*i.read().split()), "Uppercase a string")

def test_public_ci_all():
    ci = CommandInterpreter()
    register_commands(ci)
    # multiplication
    assert run_command_and_capture(ci, "mul 6 7") == "42\n"
    assert run_command_and_capture(ci, "mul 13 3") == "39\n"
    # decrement
    assert run_command_and_capture(ci, "dec 100") == "99\n"
    assert run_command_and_capture(ci, "dec -10") == "-11\n"
    # triple
    assert run_command_and_capture(ci, "triple 8") == "24\n"
    assert run_command_and_capture(ci, "triple -5") == "-15\n"
    # upper
    assert run_command_and_capture(ci, "upper publicTest") == "PUBLICTEST\n"
    assert run_command_and_capture(ci, "upper differEnt") == "DIFFERENT\n"

    # help output
    got = run_command_and_capture(ci, "help")
    expected = (
        "mul    Multiply two numbers\n"
        "dec    Decrement a number\n"
        "triple Triple a number\n"
        "upper  Uppercase a string\n"
        "help   Show this help\n"
    )
    def norm(s):
        import re
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

    assert run_command_and_capture(ci, "foo 123") == "Unknown command: foo\n"
    assert run_command_and_capture(ci, "") == ""