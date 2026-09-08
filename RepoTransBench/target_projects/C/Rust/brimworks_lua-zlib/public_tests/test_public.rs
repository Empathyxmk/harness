// Translated from test_public.lua

use lua_zlib::*;
use std::fs::File;
use std::io::{Read};

fn read_file_as_bytes(path: &str) -> Vec<u8> {
    let mut v = Vec::new();
    let mut f = File::open(path).expect(&format!("open file: {}", path));
    f.read_to_end(&mut v).expect("read file as bytes");
    v
}

#[test]
fn test_amnon_david_public() {
    let gz_path = "./amnon_david.gz";
    if std::path::Path::new(gz_path).exists() {
        let deflated = read_file_as_bytes(gz_path);
        let inflated = inflate(&deflated).expect("inflate amnon_david.gz");
        assert_eq!(
            &inflated[0..10],
            "Amnon Davi",
            "inflate file amnon_david.gz first 10 bytes"
        );
    }
}

#[test]
fn test_roundtrip_public() {
    let orig = "public_test_case_lua_zlib_2024";
    let deflated = deflate(orig, None).unwrap();
    let inflated = inflate(&deflated).expect("deflate+inflate roundtrip");
    assert_eq!(inflated, orig, "deflate+inflate roundtrip for alt string");
}

#[test]
fn test_table_concat_public() {
    let mut t = Vec::new();
    for i in 1..=20 {
        t.push(format!("{}", i % 5));
    }
    let s = t.join("|");
    let deflated = deflate(&s, None).unwrap();
    let orig = inflate(&deflated).unwrap();
    assert_eq!(orig, s, "inflate deflated table-concat string for new data");
}