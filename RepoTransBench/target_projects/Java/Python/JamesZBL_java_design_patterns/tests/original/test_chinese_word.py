import sys
import io

class Character:
    def __init__(self, ch=None):
        self.ch = ch
    def print(self):
        pass

class ChineseWord:
    def __init__(self, chars):
        self.chars = chars
    def count(self):
        return len(self.chars)
    def print_before(self):
        print("", end="")

def test_constructor_and_print_before():
    c = Character()
    word = ChineseWord([c])
    assert word.count() == 1
    out = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = out
    word.print_before()
    sys.stdout = sys_stdout
    assert out.getvalue() == ""