package public_tests

import (
    "reflect"
    "testing"
    "owncloudpyocclient/owncloud"
)

func TestIsFilePublic(t *testing.T) {
    tests := []struct{
        path string
        want bool
    }{
        {"/docs/readme.md", true},
        {"song.mp3", true},
        {"/folder1/test.csv", true},
        {"/folder1/subdir/", false},
        {"/anotherdir/", false},
    }
    for _, tc := range tests {
        got := owncloud.IsFile(tc.path)
        if got != tc.want {
            t.Errorf("IsFile(%q) = %v; want %v", tc.path, got, tc.want)
        }
    }
}

func TestStripTrailingSlashPublic(t *testing.T) {
    cases := []struct{ s, want string }{
        {"/tmp/testcase/", "/tmp/testcase"},
        {"/foo/bar/long/path/", "/foo/bar/long/path"},
        {"/bar/xx", "/bar/xx"},
        {"/", ""},
    }
    for _, tc := range cases {
        got := owncloud.StripTrailingSlashPub(tc.s)
        if got != tc.want {
            t.Errorf("StripTrailingSlashPub(%q) = %q; want %q", tc.s, got, tc.want)
        }
    }
}

func TestParseDavResponseValidPublic(t *testing.T) {
    xml_response := `<?xml version="1.0" encoding="utf-8"?>
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
    `
    got := owncloud.ParseDavResponse(xml_response)
    want := [][2]interface{}{
        {"/remote.php/dav/files/bar/doc.md", map[string]string{"getcontentlength": "999"}},
        {"/remote.php/dav/files/bar/image.jpeg", map[string]string{"getcontentlength": "2048"}},
    }
    if !reflect.DeepEqual(got, want) {
        t.Errorf("ParseDavResponse got = %v, want %v", got, want)
    }
}

func TestParseDavResponseEmptyPublic(t *testing.T) {
    xml_response := `<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:"></d:multistatus>
    `
    got := owncloud.ParseDavResponse(xml_response)
    want := [][2]interface{}{}
    if !reflect.DeepEqual(got, want) {
        t.Errorf("ParseDavResponse got = %v, want %v", got, want)
    }
}

func TestEnsureLeadingSlashPublic(t *testing.T) {
    cases := []struct{s string; want string}{
        {"new/path", "/new/path"},
        {"/starts/with/slash", "/starts/with/slash"},
        {"", "/"},
    }
    for _, tc := range cases {
        got := owncloud.EnsureLeadingSlash(tc.s)
        if got != tc.want {
            t.Errorf("EnsureLeadingSlash(%q) = %q; want %q", tc.s, got, tc.want)
        }
    }
}

func TestStripLeadingSlashPublic(t *testing.T) {
    cases := []struct{s string; want string}{
        {"/strip/me", "strip/me"},
        {"already/stripped", "already/stripped"},
        {"/", ""},
    }
    for _, tc := range cases {
        got := owncloud.StripLeadingSlash(tc.s)
        if got != tc.want {
            t.Errorf("StripLeadingSlash(%q) = %q; want %q", tc.s, got, tc.want)
        }
    }
}

func TestUnicodeUrlquotePublic(t *testing.T) {
    url := owncloud.UnicodeUrlQuote("日本語ファイル.txt")
    if url != "%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB.txt" {
        t.Errorf("UnicodeUrlQuote returned wrong value: %s", url)
    }
    url2 := owncloud.UnicodeUrlQuote("plik_żółw.txt")
    if url2 != "plik_%C5%BC%C3%B3%C5%82w.txt" {
        t.Errorf("UnicodeUrlQuote returned wrong value: %s", url2)
    }
}

func TestContentRangeUtilityPublic(t *testing.T) {
    cases := []struct{start, end, total int; want string}{
        {10, 29, 120, "bytes 10-29/120"},
        {200, 400, 1000, "bytes 200-400/1000"},
        {3, 7, 9, "bytes 3-7/9"},
    }
    for _, tc := range cases {
        got := owncloud.ContentRange(tc.start, tc.end, tc.total)
        if got != tc.want {
            t.Errorf("ContentRange(%d,%d,%d) = %q; want %q", tc.start, tc.end, tc.total, got, tc.want)
        }
    }
}

func TestStripPrefixPublic(t *testing.T) {
    cases := []struct{s, prefix, want string}{
        {"/api/v3/data", "/api/v3/", "data"},
        {"api/v1/resource", "api/v1/", "resource"},
        {"foo/bar", "foo/", "bar"},
        {"nomatch", "x/", "nomatch"},
    }
    for _, tc := range cases {
        got := owncloud.StripPrefix(tc.s, tc.prefix)
        if got != tc.want {
            t.Errorf("StripPrefix(%q, %q) = %q; want %q", tc.s, tc.prefix, got, tc.want)
        }
    }
}