class Character:
    def __init__(self, ch=None):
        self.ch = ch
    def print(self):
        pass

class CharacterComposite:
    def __init__(self, chars):
        self.chars = chars
    def count(self):
        return len(self.chars)

class EnglishWord(CharacterComposite):
    def print_before(self):
        print(" ", end="")

def test_construction_and_print_before_other_value():
    word = EnglishWord([
        Character('P'), Character('u'), Character('b'), Character('l'), Character('i'), Character('c')
    ])
    assert word.count() == 6
    # Just check it doesn't error to call print_before
    word.print_before()