import io
import sys
import types
import logging
import builtins
import pytest

from gscholar import gscholar

def test_public_get_links_bibtex():
    html = '<a href="https://scholar.googleusercontent.com/scholar.bib?baz&amp;qux">'
    links = gscholar.get_links(html, gscholar.FORMAT_BIBTEX)
    assert isinstance(links, list)
    assert links
    assert links[0].startswith('/scholar.bib?')

def test_public_get_links_endnote():
    html = '<a href="https://scholar.googleusercontent.com/scholar.enw?abc">'
    links = gscholar.get_links(html, gscholar.FORMAT_ENDNOTE)
    assert links == ['/scholar.enw?abc']

def test_public_get_links_refman():
    html = '<a href="https://scholar.googleusercontent.com/scholar.ris?xyz">'
    links = gscholar.get_links(html, gscholar.FORMAT_REFMAN)
    assert links == ['/scholar.ris?xyz']

def test_public_get_links_wenxianwang():
    html = '<a href="https://scholar.googleusercontent.com/scholar.ral?lmn">'
    links = gscholar.get_links(html, gscholar.FORMAT_WENXIANWANG)
    assert links == ['/scholar.ral?lmn']

def test_public_convert_pdf_to_txt(monkeypatch):
    def fake_popen(cmd, stdout):
        class FakeProc:
            def communicate(self):
                return [b'ALTERNATE_PDF_CONTENT']
        return FakeProc()
    monkeypatch.setattr(gscholar.subprocess, "Popen", fake_popen)
    result = gscholar.convert_pdf_to_txt("another.pdf", startpage=3)
    assert "ALTERNATE_PDF_CONTENT" in result

def test_public_convert_pdf_to_txt_no_startpage(monkeypatch):
    def fake_popen(cmd, stdout):
        class FakeProc:
            def communicate(self):
                return [b'AltContent']
        return FakeProc()
    monkeypatch.setattr(gscholar.subprocess, "Popen", fake_popen)
    result = gscholar.convert_pdf_to_txt("b.pdf")
    assert "AltContent" in result

def test_public_query_fetch_links(monkeypatch):
    search_result_link = '/scholar.bib?public'
    class DummyResponse:
        def __init__(self, html):
            self.html = html.encode('utf8')
            self.headers = {'Set-Cookie': ';X=Y;'}
        def read(self):
            return self.html
    step = {'n': 0}
    def fake_urlopen(request):
        if step['n'] == 0:
            step['n'] += 1
            return DummyResponse(f'<a href="https://scholar.googleusercontent.com{search_result_link}">')
        else:
            return DummyResponse('@inproceedings{...otherbibtex...}')
    def fake_get_links(html, outformat):
        return [search_result_link]
    monkeypatch.setattr(gscholar, 'get_links', fake_get_links)
    monkeypatch.setattr(gscholar, 'urlopen', fake_urlopen)
    monkeypatch.setattr(gscholar, 'Request', lambda url, headers=None: url)
    results = gscholar.query("alternate search", outformat=gscholar.FORMAT_BIBTEX)
    assert results
    assert "@inproceedings" in results[0]

def test_public_query_allresults(monkeypatch):
    search_result_link = '/scholar.bib?public'
    class DummyResponse:
        def __init__(self, html):
            self.html = html.encode('utf8')
            self.headers = {'Set-Cookie': ';X=Y;'}
        def read(self):
            return self.html
    step = {'n': 0}
    def fake_urlopen(request):
        if step['n'] == 0:
            step['n'] += 1
            return DummyResponse(f'<a href="https://scholar.googleusercontent.com{search_result_link}">')
        else:
            return DummyResponse('@inproceedings{...otherbibtex...}')
    def fake_get_links(html, outformat):
        return [search_result_link, search_result_link]
    monkeypatch.setattr(gscholar, 'get_links', fake_get_links)
    monkeypatch.setattr(gscholar, 'urlopen', fake_urlopen)
    monkeypatch.setattr(gscholar, 'Request', lambda url, headers=None: url)
    results = gscholar.query("alternate search", outformat=gscholar.FORMAT_BIBTEX, allresults=True)
    assert len(results) == 2
    assert all("@inproceedings" in r for r in results)

def test_public_import_all_and_version():
    import gscholar
    assert hasattr(gscholar, 'query')
    assert hasattr(gscholar, '__VERSION__')

def test_public_logger_debug(monkeypatch, caplog):
    with caplog.at_level(logging.DEBUG):
        gscholar.logger.debug("public debug")