import sys
import os
import types
import builtins
import io
import pytest

import gscholar.__main__ as gscholar_main
import gscholar

def make_fake_args(args: list):
    sys.argv = ["prog"] + args

def test_main_version(monkeypatch, capsys):
    make_fake_args(['--version', 'test'])
    with pytest.raises(SystemExit) as excinfo:
        gscholar_main.main()
    assert excinfo.value.code == 0

def test_main_search(monkeypatch, capsys):
    output_val = ['somebibtex']
    def fake_query(keyword, outformat, all_):
        assert keyword == "my search"
        return output_val
    monkeypatch.setattr(gscholar, 'query', fake_query)
    make_fake_args(['-f', 'bibtex', "my search"])
    out = io.StringIO()
    sys.stdout = out
    gscholar_main.main()
    sys.stdout = sys.__stdout__
    assert "somebibtex" in out.getvalue()

def test_main_search_no_results(monkeypatch):
    def fake_query(keyword, outformat, all_):
        return []
    monkeypatch.setattr(gscholar, 'query', fake_query)
    make_fake_args(['-f', 'bibtex', "xsearch"])
    with pytest.raises(SystemExit) as excinfo:
        gscholar_main.main()
    assert excinfo.value.code == 1

def test_main_rename_pdf(monkeypatch):
    bib = ['somebib']
    called = {}
    def fake_pdflookup(pdf, all_, outformat, startpage):
        assert pdf == "afile.pdf"
        called['l'] = True
        return bib
    def fake_rename_file(f, bibentry):
        called['r'] = (f, bibentry)
    def fake_exists(x):
        return x == "afile.pdf"
    monkeypatch.setattr(gscholar, 'pdflookup', fake_pdflookup)
    monkeypatch.setattr(gscholar, 'rename_file', fake_rename_file)
    monkeypatch.setattr(os.path, 'exists', fake_exists)
    make_fake_args(["-f", "bibtex", "--rename", "afile.pdf"])
    sys.stdout = io.StringIO()
    gscholar_main.main()
    sys.stdout = sys.__stdout__
    assert called['l'] and called['r'][0] == "afile.pdf"

def test_main_rename_no_pdf(monkeypatch, capsys):
    def fake_query(keyword, outformat, all_):
        return ['foo']
    monkeypatch.setattr(gscholar, 'query', fake_query)
    monkeypatch.setattr(os.path, 'exists', lambda x: False)
    make_fake_args(["-f", "bibtex", "--rename", "notafile"])
    with pytest.raises(SystemExit) as excinfo:
        gscholar_main.main()
    sys.stdout = sys.__stdout__
    assert excinfo.value.code == 1

def test_main_all(monkeypatch):
    results = ["bib1", "bib2"]
    def fake_query(keyword, outformat, all_):
        return results
    monkeypatch.setattr(gscholar, 'query', fake_query)
    make_fake_args(["-f", "bibtex", "--all", "somesearch"])
    out = io.StringIO()
    sys.stdout = out
    gscholar_main.main()
    sys.stdout = sys.__stdout__
    val = out.getvalue()
    assert "bib1" in val and "bib2" in val

def test_main_output_formats(monkeypatch):
    exp = []
    def fake_query(keyword, outformat, all_):
        exp.append(outformat)
        return ['bibX']
    monkeypatch.setattr(gscholar, 'query', fake_query)
    for fmt, val in [("endnote", gscholar.FORMAT_ENDNOTE),
                     ("refman", gscholar.FORMAT_REFMAN),
                     ("wenxianwang", gscholar.FORMAT_WENXIANWANG)]:
        make_fake_args(["-f", fmt, "abc"])
        io_out = io.StringIO()
        sys.stdout = io_out
        gscholar_main.main()
        sys.stdout = sys.__stdout__
    assert gscholar.FORMAT_ENDNOTE in exp
    assert gscholar.FORMAT_REFMAN in exp
    assert gscholar.FORMAT_WENXIANWANG in exp