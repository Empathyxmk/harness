import pytest

class ContentDetector:
    """
    Simulates the Java ContentDetector.
    - clues: list of lists, each sublist is a set of 'all must be present' terms, any sublist is ORred.
    - max_offset: only scan first N bytes
    """
    def __init__(self, clues, max_offset):
        self.clues = clues
        self.max_offset = max_offset

    def getFirstMatch(self, content_bytes):
        text = content_bytes[:self.max_offset].decode('utf-8', errors='ignore')
        for idx, clue_group in enumerate(self.clues):
            if all(clue in text for clue in clue_group):
                return idx
        return -1

    def matches(self, content_bytes):
        return self.getFirstMatch(content_bytes) != -1

def test_simple_or_match():
    clues = [["foo"], ["bar"]]
    detector = ContentDetector(clues, 100)
    assert detector.getFirstMatch("foo hello world".encode('utf-8')) == 0
    assert detector.getFirstMatch("something bar here".encode('utf-8')) == 1
    assert detector.getFirstMatch("baz qux".encode('utf-8')) == -1

def test_and_match():
    clues = [["foo", "bar"], ["baz"]]
    detector = ContentDetector(clues, 100)
    assert detector.getFirstMatch("this line has foo and bar together".encode('utf-8')) == 0
    assert detector.getFirstMatch("some baz string".encode('utf-8')) == 1
    assert detector.getFirstMatch("foo only here".encode('utf-8')) == -1

def test_max_offset():
    clues = [["clue"]]
    detector = ContentDetector(clues, 4)
    # only first 4 bytes; 'clue' begins at offset 7 in "say clue later"
    assert detector.getFirstMatch("say clue later".encode('utf-8')) == -1
    assert detector.getFirstMatch("clue here".encode('utf-8')) == 0

def test_matches_convenience():
    clues = [["needle"]]
    detector = ContentDetector(clues, 100)
    assert detector.matches("and a needle in haystack".encode('utf-8')) is True
    assert detector.matches("no match".encode('utf-8')) is False