use owncloud_pyocclient::owncloud::*;
use std::collections::HashMap;

#[test]
fn test_is_file_public() {
    assert_eq!(_is_file("/docs/readme.md"), true);
    assert_eq!(_is_file("song.mp3"), true);
    assert_eq!(_is_file("/folder1/test.csv"), true);
    assert_eq!(_is_file("/folder1/subdir/"), false);
    assert_eq!(_is_file("/anotherdir/"), false);
}

#[test]
fn test_strip_trailing_slash_public() {
    assert_eq!(_strip_trailing_slash("/tmp/testcase/"), "/tmp/testcase");
    assert_eq!(_strip_trailing_slash("/foo/bar/long/path/"), "/foo/bar/long/path");
    assert_eq!(_strip_trailing_slash("/bar/xx"), "/bar/xx");
    assert_eq!(_strip_trailing_slash("/"), "");
}

#[test]
fn test_parse_dav_response_valid_public() {
    let xml_response = r#"<?xml version="1.0" encoding="utf-8"?>
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
    "#;
    let result = _parse_dav_response(xml_response);
    let mut expected1 = HashMap::new();
    expected1.insert("getcontentlength".to_string(), "999".to_string());
    let mut expected2 = HashMap::new();
    expected2.insert("getcontentlength".to_string(), "2048".to_string());
    assert_eq!(result.len(), 2);
    assert_eq!(result[0], ("/remote.php/dav/files/bar/doc.md".to_string(), expected1));
    assert_eq!(result[1], ("/remote.php/dav/files/bar/image.jpeg".to_string(), expected2));
}

#[test]
fn test_parse_dav_response_empty_public() {
    let xml_response = r#"<?xml version="1.0" encoding="utf-8"?>
    <d:multistatus xmlns:d="DAV:"></d:multistatus>
    "#;
    let result = _parse_dav_response(xml_response);
    assert_eq!(result.len(), 0);
}

#[test]
fn test_ensure_leading_slash_public() {
    assert_eq!(_ensure_leading_slash("new/path"), "/new/path");
    assert_eq!(_ensure_leading_slash("/starts/with/slash"), "/starts/with/slash");
    assert_eq!(_ensure_leading_slash(""), "/");
}

#[test]
fn test_strip_leading_slash_public() {
    assert_eq!(_strip_leading_slash("/strip/me"), "strip/me");
    assert_eq!(_strip_leading_slash("already/stripped"), "already/stripped");
    assert_eq!(_strip_leading_slash("/"), "");
}

#[test]
fn test_unicode_urlquote_public() {
    let url = _unicode_urlquote("日本語ファイル.txt");
    assert_eq!(url, "%E6%97%A5%E6%9C%AC%E8%AA%9E%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB.txt");
    let url2 = _unicode_urlquote("plik_żółw.txt");
    assert_eq!(url2, "plik_%C5%BC%C3%B3%C5%82w.txt");
}

#[test]
fn test_content_range_utility_public() {
    assert_eq!(_content_range(10, 29, 120), "bytes 10-29/120");
    assert_eq!(_content_range(200, 400, 1000), "bytes 200-400/1000");
    assert_eq!(_content_range(3, 7, 9), "bytes 3-7/9");
}

#[test]
fn test_strip_prefix_public() {
    assert_eq!(_strip_prefix("/api/v3/data", "/api/v3/"), "data");
    assert_eq!(_strip_prefix("api/v1/resource", "api/v1/"), "resource");
    assert_eq!(_strip_prefix("foo/bar", "foo/"), "bar");
    assert_eq!(_strip_prefix("nomatch", "x/"), "nomatch");
}