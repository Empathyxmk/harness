import io
import sys

class CharacterComposite:
    def __init__(self, count_val=0):
        self._count = count_val
    def count(self):
        return self._count
    def print(self):
        pass

class Writer:
    def sentence_by_chinese(self):
        return StubChineseSentence()
    def sentence_by_english(self):
        return StubEnglishSentence()

class StubChineseSentence(CharacterComposite):
    def __init__(self):
        super().__init__(count_val=7)
    def print(self):
        print("我是来自北京的小明。", end="")

class StubEnglishSentence(CharacterComposite):
    def __init__(self):
        super().__init__(count_val=6)
    def print(self):
        print("I am a student from London.", end="")

def test_sentence_by_chinese_public():
    writer = Writer()
    test_writer_cn(writer.sentence_by_chinese(), "我是来自北京的小明。")

def test_sentence_by_english_public():
    writer = Writer()
    test_writer_trimmed(writer.sentence_by_english(), "I am a student from London.")

def test_writer_trimmed(given_composite, expected_string):
    words = expected_string.strip().split(" ")
    assert given_composite is not None
    assert given_composite.count() == len(words)
    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf
    given_composite.print()
    sys.stdout = sys_stdout
    output = buf.getvalue().strip().lower()
    expected = expected_string.strip().lower()
    assert output.endswith(".")
    assert expected == output

def test_writer_cn(given_composite, expected_string):
    assert given_composite is not None
    buf = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = buf
    given_composite.print()
    sys.stdout = sys_stdout
    output = buf.getvalue().strip()
    assert "北京" in output
    assert output.endswith("。")