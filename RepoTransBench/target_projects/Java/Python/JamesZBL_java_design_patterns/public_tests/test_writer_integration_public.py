import io
import sys

class Writer:
    def sentence_by_english(self):
        return StubEnglishSentence()

class StubEnglishSentence:
    def print(self):
        print("I am a student from London.", end="")

def test_writer_sentences_public():
    baos = io.StringIO()
    sys_stdout = sys.stdout
    sys.stdout = baos
    Writer().sentence_by_english().print()
    sys.stdout = sys_stdout
    result = baos.getvalue()
    assert "student" in result
    assert "from" in result