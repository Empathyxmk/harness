// Translated from test_zlib_edge.lua

use lua_zlib::*;

#[test]
fn test_deflate_inflate_empty() {
    let compressed = deflate("", Some(9)).expect("deflate empty string");
    let decompressed = inflate(&compressed).expect("inflate empty string");
    assert_eq!(decompressed, "", "inflate empty string");
}

#[test]
fn test_inflate_invalid_fails() {
    let invalid = b"notzlibdata";
    let result = inflate(invalid);
    assert!(result.is_err(), "inflate invalid fails as expected");
}

#[test]
fn test_compress_decompress_1mb() {
    let big = "a".repeat(1024 * 1024);
    let compbig = deflate(&big, Some(6)).expect("deflate 1MB");
    let decbig = inflate(&compbig).expect("inflate 1MB");
    assert_eq!(decbig, big, "compress/decompress 1MB");
}