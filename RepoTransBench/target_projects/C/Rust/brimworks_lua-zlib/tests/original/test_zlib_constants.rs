// Translated from test_zlib_constants.lua

use lua_zlib::*;

#[test]
fn test_meta_fields_present() {
    let fields = [
        _COPYRIGHT,
        _DESCRIPTION,
        _VERSION,
    ];
    for field in &fields {
        assert!(!field.is_empty(), "meta field not empty: {}", field);
    }
    assert!(BEST_SPEED != 0, "BEST_SPEED present");
    assert!(BEST_COMPRESSION != 0, "BEST_COMPRESSION present");
}

#[test]
fn test_optional_fields() {
    // These values are always present in our translation
    assert!(NO_COMPRESSION == 0, "NO_COMPRESSION is 0");
    let _ = DEFAULT_COMPRESSION;
    let _ = FILTERED;
    let _ = HUFFMAN_ONLY;
    let _ = RLE;
    let _ = FIXED;
    let _ = DEFAULT_STRATEGY;
}

#[test]
fn test_version_returns_string() {
    let v = version();
    assert!(!v.is_empty(), "zlib.version() returns string");
}