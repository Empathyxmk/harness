// Translated from test_zlib_edge_public.lua

use lua_zlib::*;

#[test]
fn test_single_space_deflate_inflate() {
    let compressed = deflate(" ", Some(6)).expect("deflate single space string");
    let decompressed = inflate(&compressed).expect("inflate single space string");
    assert_eq!(decompressed, " ", "inflate single space string");
}

#[test]
fn test_binary_deflate_inflate() {
    // Use binary data, not UTF-8.
    let bin: [u8; 5] = [2, 3, 4, 5, 6];
    let compressed = deflate_bytes(&bin, Some(1)).expect("deflate binary data");
    let decomp = inflate_bytes(&compressed).expect("inflate binary data");
    assert_eq!(&decomp[..], &bin[..], "inflate binary data");
}