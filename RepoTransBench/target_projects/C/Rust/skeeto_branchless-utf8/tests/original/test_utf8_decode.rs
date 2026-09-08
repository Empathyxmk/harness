// Translation of test/test_utf8_decode.c from C to Rust.

use skeeto_branchless_utf8::{utf8_decode, utf8_encode};

fn do_test_ascii() {
    let mut buf = [0u8; 4];
    buf[0] = b'A';
    let (c, e, next) = {
        let (c, e, n) = utf8_decode(&buf[..1]);
        (c, e, n)
    };
    assert_eq!(next, 1);
    assert!(!e);
    assert_eq!(c, b'A' as u32);
}

fn do_test_2byte() {
    let buf = [0xC2, 0xA2, 0, 0];
    let (c, e, next) = utf8_decode(&buf[..2]);
    assert_eq!(next, 2);
    assert!(!e);
    assert_eq!(c, 0xA2);
}

fn do_test_3byte() {
    let buf = [0xE2, 0x82, 0xAC, 0];
    let (c, e, next) = utf8_decode(&buf[..3]);
    assert_eq!(next, 3);
    assert!(!e);
    assert_eq!(c, 0x20AC);
}

fn do_test_4byte() {
    let buf = [0xF0, 0x9F, 0x98, 0x81];
    let (c, e, next) = utf8_decode(&buf[..4]);
    assert_eq!(next, 4);
    assert!(!e);
    assert_eq!(c, 0x1F601);
}

fn do_test_invalid_1() {
    let buf = [0xFF, 0, 0, 0];
    let (c, e, _next) = utf8_decode(&buf[..1]);
    let _ = c;
    assert!(e); // error expected
}

fn do_test_truncated() {
    let buf = [0xE2, 0x28, 0, 0];
    let (c, e, _next) = utf8_decode(&buf[..2]);
    let _ = c;
    assert!(e);
}

fn do_test_surrogate() {
    let buf = [0xED, 0xA0, 0x80, 0];
    let (c, e, _next) = utf8_decode(&buf[..3]);
    let _ = c;
    assert!(e);
}

#[test]
fn test_utf8_decode_all() {
    do_test_ascii();
    do_test_2byte();
    do_test_3byte();
    do_test_4byte();
    do_test_invalid_1();
    do_test_truncated();
    do_test_surrogate();
}