import pytest
from src.command_interpreter import CommandInterpreter

# Non-member function
def add(x: int, y: int) -> int:
    return x + y

class Arithmetic(CommandInterpreter):
    @staticmethod
    def inc(x: int) -> int:
        return x + 1

    def twice(self, x: int) -> int:
        return 2 * x

    def rev(self, s: str) -> str:
        return s[::-1]

    def register_commands(self):
        self.register_command(add, "add", "Add two numbers")
        self.register_command(self.inc, "inc", "Increment a number")
        self.register_command(self.twice, "twice", "Double a number")
        self.register_command(self.rev, "rev", "Reverse a string")

arithmetic = Arithmetic()

def run_test(text, expected):
    result = arithmetic.eval(text)
    assert result == expected, f"Text: {text}\nExpected: {expected}\nResult: {result}"

def test_arithmetic_commands():
    run_test("inc 17", "18")
    run_test("add 4 5\n", "9")
    run_test("twice 7", "14")
    run_test("rev Hello", "olleH")

def test_arithmetic_arg_errors():
    run_test("inc", "Error: expected 1 argument; got 0")
    run_test("inc 1 7", "Error: expected 1 argument; got 2")
    run_test("inc 1.7", "Error: invalid argument type at position 0; expected type i")

    run_test("add 4", "Error: expected 2 arguments; got 1")
    run_test("add 4 5 6", "Error: expected 2 arguments; got 3")
    run_test("add 4.4 5", "Error: invalid argument type at position 0; expected type i")
    run_test("add 4 5.5", "Error: invalid argument type at position 1; expected type i")

def test_arithmetic_help():
    # Help output is aligned, so canonicalize space
    got = arithmetic.eval("help")
    expected = ("add    Add two numbers\n"
                "inc    Increment a number\n"
                "twice  Double a number\n"
                "rev    Reverse a string\n"
                "help   Show this help")
    got_lines = got.strip().split('\n')
    exp_lines = expected.strip().split('\n')
    # Compare lines ignoring multiple spaces
    def norm(s):
        import re
        return ' '.join(s.split())
    assert [norm(g) for g in got_lines] == [norm(e) for e in exp_lines], f"Got:\n{got}\nExpected:\n{expected}"