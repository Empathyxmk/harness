// Translated from test_zlib_constants_public.lua

use lua_zlib::*;

#[test]
fn test_public_constants_present() {
    assert_eq!(NO_COMPRESSION, 0, "NO_COMPRESSION is present");
    assert_eq!(DEFAULT_COMPRESSION, 6, "DEFAULT_COMPRESSION is present");
    assert_eq!(FILTERED, 1, "FILTERED is present");
    assert_eq!(HUFFMAN_ONLY, 2, "HUFFMAN_ONLY is present");
    assert!(!_COPYRIGHT.is_empty(), "_COPYRIGHT present");
    assert!(!_DESCRIPTION.is_empty(), "_DESCRIPTION present");
}