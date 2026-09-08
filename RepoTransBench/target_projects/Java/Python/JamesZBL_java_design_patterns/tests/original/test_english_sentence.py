import sys
import io

class EnglishWord:
    def __init__(self, chars):
        self.chars = chars
    def count(self):
        return len(self.chars)
    
class EnglishSentence:
    def __init__(self, words):
        self.words = words
    def count(self):
        return len(self.words)
    def print_after(self):
        print(".")
        print()

def test_constructor_and_print_after():
    word = EnglishWord([])
    sentence = EnglishSentence([word])
    assert sentence.count() == 1
    out = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = out
    sentence.print_after()
    sys.stdout = sys_stdout
    # Remove Windows or Unix newline confusion
    assert out.getvalue().replace('\r\n', '\n') == ".\n"