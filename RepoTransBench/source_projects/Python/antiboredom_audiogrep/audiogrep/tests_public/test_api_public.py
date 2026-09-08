import audiogrep
import pytest

def test_find_files_public(tmp_path):
    # Use different extension and names than original test
    files = [
        tmp_path / "x.flac",
        tmp_path / "y.flac",
        tmp_path / "z.txt",
    ]
    for f in files:
        f.write_text("dummy")

    found = set(audiogrep.find_files(str(tmp_path), exts=[".flac"]))
    # Should only return .flac files
    assert set(found) == {str(tmp_path / "x.flac"), str(tmp_path / "y.flac")}

def test_regexify_public():
    # Use a string not in original test
    text = "hello? world* (demo)"
    r = audiogrep.regexify(text)
    # The result should be a regex string that escapes special chars
    assert r == r"hello\?\ world\*\ \(demo\)"

def test_get_word_timings_public(tmp_path):
    # Use different lines
    fn = tmp_path / "timings_public.txt"
    lines = [
        "<s> 5.0 6.0 1\n", 
        "gamma 6.0 6.2 1\n", 
        "zeta 6.2 6.3 1\n", 
        "</s> 6.3 6.7 1\n"
    ]
    fn.write_text("".join(lines))
    tgt = audiogrep.get_word_timings(str(fn))
    assert len(tgt) == 2  # Should return only middle words
    assert tgt[0][0] == "gamma"
    assert tgt[1][0] == "zeta"

def test_group_words_public():
    # Different sequence and group size
    words = [('a', 1, 2, 3), ('b', 2, 3, 4), ('c', 3, 4, 5), ('d', 4, 5, 6), ('e', 5, 6, 7)]
    n = 4
    grouped = list(audiogrep.group_words(words, n))
    assert len(grouped) == 2  # ('a','b','c','d'), ('b','c','d','e')
    assert grouped[0][0][0] == 'a'
    assert grouped[1][0][0] == 'b'

def test_get_grouped_word_timings_public(tmp_path):
    fn = tmp_path / "grouped_timings_public.txt"
    lines = [
        "<s> 11.0 12.0 1\n", 
        "x 12.0 12.44 1\n", 
        "y 12.44 12.89 1\n", 
        "z 12.89 13.41 1\n", 
        "</s> 13.41 13.91 1\n"
    ]
    fn.write_text("".join(lines))
    groups = list(audiogrep.get_grouped_word_timings(str(fn), n=2))
    assert len(groups) == 2  # ("x","y"), ("y","z")
    assert groups[0][0][0] == "x"
    assert groups[1][0][0] == "y"

def test_franken_sentence_public():
    # Use different word timings and structure
    in_wt = [
        [("apple", 0.1, 0.2, 0), ("pear", 0.2, 0.3, 0)],
        [("banana", 0.3, 0.5, 0)]
    ]
    r = audiogrep.franken_sentence("test sentence", in_wt)
    assert isinstance(r, list)
    # Should produce a list with slice-like elements for each group
    assert all(isinstance(e, slice) or isinstance(e, tuple) for e in r)

def test_search_modes_public(monkeypatch, tmp_path):
    fn = tmp_path / "public.transcription.txt"
    lines = [
        "<s> 3.0 3.7 1\n", "foo 3.7 3.8 1\n", "bar 3.8 4.1 1\n", "</s> 4.1 4.5 1\n"
    ]
    fn.write_text("".join(lines))

    # Patch the searched methods to return distinct-dummy-for-public-tests
    monkeypatch.setattr(audiogrep, "fragment_search", lambda q,s,reg: [{"X": "Y"}])
    monkeypatch.setattr(audiogrep, "word_search", lambda q,s,reg: [{"Q": 2}])
    monkeypatch.setattr(audiogrep, "franken_sentence", lambda q,fs: [42])

    # The actual audiogrep.search should dispatch
    assert audiogrep.search("any", str(fn), "fragment", False) == [{"X": "Y"}]
    assert audiogrep.search("hello", str(fn), "word", False) == [{"Q": 2}]
    assert audiogrep.search("repeat", str(fn), "sentence", False) == [42]

def test_make_splice_public(tmp_path):
    # Create dummy slices and output file
    out_mp3 = tmp_path / "f.spliced.mp3"
    slices = [slice(0, 2), slice(3, 5)]
    # Should not actually create audio, but function should run
    with pytest.raises(Exception):  # It will likely fail (no ffmpeg)
        audiogrep.make_splice("dummy.mp3", slices, str(out_mp3))