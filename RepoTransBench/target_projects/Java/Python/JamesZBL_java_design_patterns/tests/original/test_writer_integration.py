import io
import sys
import pytest

# Stubs for the composite classes, to be replaced by true implementations.
# In real translation, these should import actual code.
# For these tests, we provide enough for logic to run.

class CharacterComposite:
    def count(self):
        return 0

    def print(self):
        pass

class Writer:
    def sentence_by_chinese(self):
        return StubChineseSentence()

    def sentence_by_english(self):
        return StubEnglishSentence()

class StubChineseSentence(CharacterComposite):
    def print(self):
        print("我是来自北京的小明。", end="")

class StubEnglishSentence(CharacterComposite):
    def print(self):
        print("I am a student from London.", end="")

def test_writer_sentences():
    baos = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = baos
    Writer().sentence_by_chinese().print()
    Writer().sentence_by_english().print()
    sys.stdout = sys_stdout
    result = baos.getvalue()
    assert "." in result