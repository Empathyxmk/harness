import pytest

def func_hello(i):
    print(f"#{i} Hello")

class func_printnum_t:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __call__(self, i):
        print(f"#{i} Numbers are: {self.x}, {self.y}")

def repeattwice(func):
    func(1)
    func(2)

def test_function_outputs(capsys):
    x = 4
    y = 2
    # Lambda
    repeattwice(lambda i: print(f"#{i} Numbers are: {x}, {y}"))
    # Functor class
    func_printnum = func_printnum_t(x, y)
    repeattwice(func_printnum)
    # Standalone function
    repeattwice(func_hello)
    # Function object
    f = lambda i: print(f"i = {i}")
    f(2)
    ff = f
    ff(3)
    output = capsys.readouterr().out
    # Basic check for expected output lines
    assert "#1 Numbers are: 4, 2" in output
    assert "#2 Numbers are: 4, 2" in output
    assert "#1 Hello" in output
    assert "#2 Hello" in output
    assert "i = 2" in output
    assert "i = 3" in output