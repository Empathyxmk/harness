import io
import sys
import types
import logging
import builtins
import pytest

from gscholar import gscholar

def test_get_links_bibtex():
    html = '<a href="https://scholar.googleusercontent.com/scholar.bib?foo&amp;bar">'
    links = gscholar.get_links(html, gscholar.FORMAT_BIBTEX)
    assert isinstance(links, list)
    assert links
    assert links[0].startswith('/scholar.bib?')

def test_get_links_endnote():
    html = '<a href="https://scholar.googleusercontent.com/scholar.enw?foo">'
    links = gscholar.get_links(html, gscholar.FORMAT_ENDNOTE)
    assert links == ['/scholar.enw?foo']

def test_get_links_refman():
    html = '<a href="https://scholar.googleusercontent.com/scholar.ris?foo">'
    links = gscholar.get_links(html, gscholar.FORMAT_REFMAN)
    assert links == ['/scholar.ris?foo']

def test_get_links_wenxianwang():
    html = '<a href="https://scholar.googleusercontent.com/scholar.ral?foo">'
    links = gscholar.get_links(html, gscholar.FORMAT_WENXIANWANG)
    assert links == ['/scholar.ral?foo']

def test_convert_pdf_to_txt(monkeypatch):
    def fake_popen(cmd, stdout):
        class FakeProc:
            def communicate(self):
                return [b'FAKE PDF CONTENT']
        return FakeProc()
    monkeypatch.setattr(gscholar.subprocess, "Popen", fake_popen)
    result = gscholar.convert_pdf_to_txt("dummy.pdf", startpage=2)
    assert "FAKE PDF CONTENT" in result

def test_convert_pdf_to_txt_no_startpage(monkeypatch):
    def fake_popen(cmd, stdout):
        class FakeProc:
            def communicate(self):
                return [b'Content']
        return FakeProc()
    monkeypatch.setattr(gscholar.subprocess, "Popen", fake_popen)
    result = gscholar.convert_pdf_to_txt("x.pdf")
    assert "Content" in result

def test_query_fetch_links(monkeypatch):
    # Fake link get_links returns
    search_result_link = '/scholar.bib?test'

    # Fake urlopen that gives a dummy HTML and Set-Cookie header
    class DummyResponse:
        def __init__(self, html):
            self.html = html.encode('utf8')
            self.headers = {'Set-Cookie': ';A=B;'}
        def read(self):
            return self.html

    step = {'n': 0}
    def fake_urlopen(request):
        # First call: returns HTML with bibtex links, Next: the bibtex entry
        if step['n'] == 0:
            step['n'] += 1
            return DummyResponse(f'<a href="https://scholar.googleusercontent.com{search_result_link}">')
        else:
            return DummyResponse('@article{...bibtex...}')

    def fake_get_links(html, outformat):
        return [search_result_link]
    monkeypatch.setattr(gscholar, 'get_links', fake_get_links)
    monkeypatch.setattr(gscholar, 'urlopen', fake_urlopen)
    monkeypatch.setattr(gscholar, 'Request', lambda url, headers=None: url)
    results = gscholar.query("test search", outformat=gscholar.FORMAT_BIBTEX)
    assert results
    assert "@article" in results[0]

def test_query_allresults(monkeypatch):
    search_result_link = '/scholar.bib?test'
    class DummyResponse:
        def __init__(self, html):
            self.html = html.encode('utf8')
            self.headers = {'Set-Cookie': ';A=B;'}
        def read(self):
            return self.html
    step = {'n': 0}
    def fake_urlopen(request):
        if step['n'] == 0:
            step['n'] += 1
            return DummyResponse(f'<a href="https://scholar.googleusercontent.com{search_result_link}">')
        else:
            return DummyResponse('@article{...bibtex...}')
    def fake_get_links(html, outformat):
        return [search_result_link, search_result_link]
    monkeypatch.setattr(gscholar, 'get_links', fake_get_links)
    monkeypatch.setattr(gscholar, 'urlopen', fake_urlopen)
    monkeypatch.setattr(gscholar, 'Request', lambda url, headers=None: url)
    results = gscholar.query("test search", outformat=gscholar.FORMAT_BIBTEX, allresults=True)
    assert len(results) == 2
    assert all("@article" in r for r in results)

def test_import_all_and_version():
    import gscholar
    assert hasattr(gscholar, 'query')
    assert hasattr(gscholar, '__VERSION__')

def test_logger_debug(monkeypatch, caplog):
    # Test that logger debug doesn't crash; not functional test but for coverage
    with caplog.at_level(logging.DEBUG):
        gscholar.logger.debug("test debug")