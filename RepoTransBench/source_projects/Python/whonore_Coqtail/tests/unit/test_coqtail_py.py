import pytest
from types import SimpleNamespace
import sys

sys.path.insert(0, 'python')

import coqtail

def test_lines_and_highlights_string():
    lines, highlights = coqtail.lines_and_highlights("foo\nbar", 0)
    assert lines == ["foo", "bar"]
    assert highlights == []

def test_lines_and_highlights_tokens():
    tagged_tokens = [
        ("test", "tag1"),
        ("\nmore", "tag2"),
        ("done", None)
    ]
    lines, highlights = coqtail.lines_and_highlights(tagged_tokens, 0)
    assert lines[0].startswith("test")
    assert any(h.tag in ["tag1", "tag2"] for h in highlights)

def test_lines_and_highlights_multiline_tok():
    tagged_tokens = [
        ("abc\n", "tag3"),
        ("def", "tag4"),
        ("\njkl", None)
    ]
    lines, highlights = coqtail.lines_and_highlights(tagged_tokens, 2)
    # Should handle newline inside token
    assert lines[0].startswith("abc")
    assert lines[-1].endswith("jkl")
    assert isinstance(highlights, list)

def test_unmatched_error_repr():
    err = coqtail.UnmatchedError("(*", (2, 4))
    assert "Found unmatched" in str(err)
    assert err.range == ((2, 4), (2, 6))

def test_nodoterror():
    # Just test it exists and can be instantiated/raised
    with pytest.raises(coqtail.NoDotError):
        raise coqtail.NoDotError()

def test_PROOF_START_END_PAT():
    assert coqtail.PROOF_START_PAT.match(b"Proof")
    assert coqtail.PROOF_END_PAT.match(b"Qed")
    for end in coqtail.OPAQUE_PROOF_ENDS:
        assert isinstance(end, bytes)