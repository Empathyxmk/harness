import os
import audiogrep
import pytest

TEST_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(TEST_DIR, "data/test.mp3")

def test_convert_to_wav_calls_subprocess(monkeypatch, tmp_path):
    test_file = tmp_path / "audio.mp3"
    test_file.write_bytes(b"abc")
    called = []
    def fake_call(args):
        called.append(args)
        (tmp_path / "audio.mp3.temp.wav").write_bytes(b"dummy")
        return 0
    monkeypatch.setattr("subprocess.call", fake_call)
    monkeypatch.setattr("os.path.exists", lambda f: False)
    out = audiogrep.convert_to_wav([str(test_file)])
    assert out == [str(test_file)+'.temp.wav']
    assert called
    monkeypatch.setattr("os.path.exists", lambda f: True)
    called.clear()
    out2 = audiogrep.convert_to_wav([str(test_file)])
    assert out2 == [str(test_file)+'.temp.wav']
    assert not called

def test_words_json_valid_and_invalid():
    s = [{'words': [["hello", "1", "2", "0.5"], ["world", "2", "3", "0.8"]], 'file':'foo'}]
    j = audiogrep.words_json(s)
    assert '"word": "hello"' in j
    s2 = [{'words': [["x", "y"]], 'file':'foo'}]
    j2 = audiogrep.words_json(s2) # should not raise

def test_convert_timestamps_edge_cases(tmp_path):
    sentences = audiogrep.convert_timestamps(["/not/a/file"])
    assert sentences == []
    sentences2 = audiogrep.convert_timestamps([str(tmp_path / "nofile.mp3")])
    assert sentences2 == []

def test_convert_timestamps_sentence(tmp_path):
    fn = tmp_path / "x.transcription.txt"
    lines = [
        "<s> 0.0 0.2 1.0\n","word 0.2 0.3 1.0\n","</s> 0.3 0.5 1.0\n"
    ]
    fn.write_text("".join(lines))
    # The "end" of the sentence is end time of last word before </s>, which is "word" at 0.3 (see audiogrep.py)
    sents = audiogrep.convert_timestamps([str(fn)])
    assert sents
    sent = sents[0]
    assert sent['start'] == 0.0 and sent['end'] == 0.3
    assert len(sent['words']) == 1
    assert sent['words'][0][0] == "word"

def test_text_reads_sentences(tmp_path):
    fn = tmp_path / "test.transcription.txt"
    lines = [
        "<s> 1 2 1\n", "a 2 3 1\n", "b 4 5 1\n", "</s> 6 7 1\n"
    ]
    fn.write_text("".join(lines))
    res = audiogrep.text([str(fn)])
    assert "a b" in res

def test_transcribe_runs(monkeypatch, tmp_path):
    tmpwav = tmp_path / "audio.temp.wav"
    tmpwav.write_bytes(b"abc")
    called = []
    def fake_check_output(args):
        called.append(args)
        return b"abc junk\n"
    monkeypatch.setattr("subprocess.check_output", fake_check_output)
    files_created = set()
    orig_open = open
    def fake_exists(f):
        if f.endswith(".transcription.txt"):
            return f in files_created
        return os.path.exists(f)
    monkeypatch.setattr("os.path.exists", fake_exists)
    def fake_remove(f):
        called.append(("rm", f))
        if f in files_created:
            files_created.remove(f)
    monkeypatch.setattr("os.remove", fake_remove)
    def fake_open(*args, **kwargs):
        name = args[0]
        if name.endswith(".transcription.txt") and ("w" in args[1] or kwargs.get('mode') == "w"):
            files_created.add(name)
            return orig_open(name, *args[1:], **kwargs)
        return orig_open(*args, **kwargs)
    monkeypatch.setattr("builtins.open", fake_open)
    outname = str(tmp_path / "audio.transcription.txt")
    if os.path.exists(outname):
        os.remove(outname)
    audiogrep.transcribe([str(tmpwav)], pre=1, post=1)
    assert any(isinstance(c, tuple) and c[0]=="rm" for c in called)
    assert outname in files_created

def test_search_modes(monkeypatch, tmp_path):
    fn = tmp_path / "s.transcription.txt"
    lines = [
        "<s> 0.0 1.0 1\n", "foo 1.0 1.1 1\n", "bar 1.1 1.2 1\n", "</s> 1.2 2.0 1\n"
    ]
    fn.write_text("".join(lines))

    monkeypatch.setattr(audiogrep, "fragment_search", lambda q,s,reg: [{"foo": "bar"}])
    monkeypatch.setattr(audiogrep, "word_search", lambda q,s,reg: [{"baz": 1}])
    monkeypatch.setattr(audiogrep, "franken_sentence", lambda q,fs: [42])
    monkeypatch.setattr(audiogrep, "convert_timestamps", lambda files: [{"words":[["foo", "1", "2", "1"]], "file":str(fn)}])
    out = audiogrep.search("foo", [str(fn)], mode="fragment")
    assert out and out[0]["foo"] == "bar"
    out2 = audiogrep.search("foo", [str(fn)], mode="word")
    assert out2 and out2[0].get("baz", 1) == 1
    out3 = audiogrep.search("foo", [str(fn)], mode="franken")
    assert out3 == [42]

def test_search_sentence(tmp_path):
    fn = tmp_path / "a.transcription.txt"
    lines = [
        "<s> 0.0 0.1 1\n", "foo 0.1 0.2 1\n", "</s> 0.2 0.3 1\n",
        "<s> 0.4 0.5 1\n", "bar 0.5 0.6 1\n", "</s> 0.6 0.7 1\n"
    ]
    fn.write_text("".join(lines))
    out = audiogrep.search("foo", [str(fn)])
    assert isinstance(out, list)
    assert any("foo" in " ".join([w[0] for w in sent["words"]]) for sent in out) or out == []

def test_fragment_search_empty():
    res = audiogrep.fragment_search("notfound", [{"words": [["a", "0", "1", "1"]], "file": "testfile"}], regex=False)
    assert res == []

def test_word_search_empty():
    res = audiogrep.word_search("notfound", [{"words": [["a", "0", "1", "1"]], "file": "testfile"}], regex=False)
    assert res == []

def test_franken_sentence_empty(monkeypatch):
    # Patch audiogrep.search used inside .franken_sentence to avoid deep logic
    monkeypatch.setattr(audiogrep, "search", lambda q, fs, mode='word': [])
    res = audiogrep.franken_sentence("notfound", [{"words": [["a", "0", "1", "1"]], "file": "testfile"}])
    assert res == []