class Character:
    def __init__(self, ch=None):
        self.ch = ch

class ChineseWord:
    def __init__(self, chars):
        self.chars = chars
    def count(self):
        return len(self.chars)

def test_chinese_word_with_other_characters():
    c1 = Character('我')
    c2 = Character('们')
    word = ChineseWord([c1, c2])
    assert word.count() == 2