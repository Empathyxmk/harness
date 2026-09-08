import sys
import os
import pytest

# Ensure the owncloud package is on sys.path and importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from owncloud import owncloud as oc

def test_is_file_public():
    assert oc._is_file("/docs/readme.md") is True
    assert oc._is_file("song.mp3") is True
    assert oc._is_file("/folder1/test.csv") is True
    assert oc._is_file("/folder1/subdir/") is False
    assert oc._is_file("/anotherdir/") is False

def test_strip_trailing_slash_public():
    assert oc._strip_trailing_slash("/tmp/testcase/") == "/tmp/testcase"
    assert oc._strip_trailing_slash("/foo/bar/long/path/") == "/foo/bar/long/path"
    assert oc._strip_trailing_slash("/bar/xx") == "/bar/xx"
    assert oc._strip_trailing_slash("/") == ""

def test_parse_dav_response_valid_public():
    xml_response = """<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:">
      <d:response>
        <d:href>/remote.php/dav/files/bar/doc.md</d:href>
        <d:propstat>
          <d:prop>
            <d:getcontentlength>999</d:getcontentlength>
          </d:prop>
        </d:propstat>
      </d:response>
      <d:response>
        <d:href>/remote.php/dav/files/bar/image.jpeg</d:href>
        <d:propstat>
          <d:prop>
            <d:getcontentlength>2048</d:getcontentlength>
          </d:prop>
        </d:propstat>
      </d:response>
    </d:multistatus>
    """
    result = oc._parse_dav_response(xml_response)
    assert result == [
        ("/remote.php/dav/files/bar/doc.md", {"getcontentlength": "999"}),
        ("/remote.php/dav/files/bar/image.jpeg", {"getcontentlength": "2048"}),
    ]

def test_parse_dav_response_empty_public():
    xml_response = """<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:"></d:multistatus>
    """
    result = oc._parse_dav_response(xml_response)
    assert result == []

def test_ensure_leading_slash_public():
    assert oc._ensure_leading_slash("new/path") == "/new/path"
    assert oc._ensure_leading_slash("/starts/with/slash") == "/starts/with/slash"
    assert oc._ensure_leading_slash("") == "/"

def test_strip_leading_slash_public():
    assert oc._strip_leading_slash("/strip/me") == "strip/me"
    assert oc._strip_leading_slash("already/stripped") == "already/stripped"
    assert oc._strip_leading_slash("/") == ""

def test_unicode_urlquote_public():
    url = oc._unicode_urlquote("日本語ファイル.txt")
    assert url == "%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB.txt"
    url2 = oc._unicode_urlquote("plik_żółw.txt")
    assert url2 == "plik_%C5%BC%C3%B3%C5%82w.txt"

def test_content_range_utility_public():
    assert oc._content_range(10, 29, 120) == "bytes 10-29/120"
    assert oc._content_range(200, 400, 1000) == "bytes 200-400/1000"
    assert oc._content_range(3, 7, 9) == "bytes 3-7/9"

def test_strip_prefix_public():
    assert oc._strip_prefix('/api/v3/data', '/api/v3/') == 'data'
    assert oc._strip_prefix('api/v1/resource', 'api/v1/') == 'resource'
    assert oc._strip_prefix('foo/bar', 'foo/') == 'bar'
    assert oc._strip_prefix('nomatch', 'x/') == 'nomatch'