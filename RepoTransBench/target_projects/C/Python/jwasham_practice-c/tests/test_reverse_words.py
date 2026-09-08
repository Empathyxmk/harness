import pytest

def reverseWords(s: str) -> str:
    """Reverse the words, keeping spaces in their place as in C sample."""
    chars = list(s)
    slen = len(chars)
    buffer = []
    tokenReadPos = slen - 1
    while tokenReadPos >= 0:
        if chars[tokenReadPos] == ' ':
            buffer.append(' ')
            tokenReadPos -= 1
        else:
            wordEnd = tokenReadPos
            while tokenReadPos >= 0 and chars[tokenReadPos] != ' ':
                tokenReadPos -= 1
            wordReadPos = tokenReadPos + 1
            while wordReadPos <= wordEnd:
                buffer.append(chars[wordReadPos])
                wordReadPos += 1
    return ''.join(buffer)

def test_reverseWords_basic():
    s = "My kingdom for a horse."
    result = reverseWords(s)
    assert result == "horse. a for kingdom My"

def test_reverseWords_empty():
    s = ""
    result = reverseWords(s)
    assert result == ""

def test_reverseWords_spaces():
    s = " This is  spaced "
    result = reverseWords(s)
    assert result == " spaced  is This "

def test_reverseWords_failure():
    s = "a"
    assert reverseWords(s) == "a"