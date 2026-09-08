class Character:
    def __init__(self, ch=None):
        self.ch = ch
    def print(self):
        pass

class EnglishWord:
    def __init__(self, chars):
        self.chars = chars
    def count(self):
        return len(self.chars)
    def print(self):
        pass

class EnglishSentence:
    def __init__(self, words):
        self.words = words
    def count(self):
        return len(self.words)
    def print(self):
        print("Test Public.", end="")

def test_sentence_composition_public():
    word1 = EnglishWord([Character('T'), Character('e'), Character('s'), Character('t')])
    word2 = EnglishWord([Character('P'), Character('u'), Character('b'), Character('l'), Character('i'), Character('c')])
    sentence = EnglishSentence([word1, word2])
    assert sentence.count() == 2
    import io, sys
    baos = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = baos
    sentence.print()
    sys.stdout = sys_stdout
    assert "." in baos.getvalue()