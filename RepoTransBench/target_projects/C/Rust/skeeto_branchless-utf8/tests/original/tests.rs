// Translation of test/tests.c from C to Rust.

use skeeto_branchless_utf8::{utf8_decode, utf8_encode};

fn is_surrogate(ch: u32) -> bool {
    ch >= 0xD800 && ch <= 0xDFFF
}

/// Test that all valid codepoints can be encoded and decoded
fn test_decode_all() {
    let mut failures = 0;
    let mut buf = [0u8; 8];
    for i in 0..=0x10FFFFu32 {
        if !is_surrogate(i) {
            let len = utf8_encode(&mut buf, i);
            if len == 0 { continue; }
            let (c, e, n) = utf8_decode(&buf[..len]);
            if n != len || c != i || e {
                failures += 1;
            }
        }
    }
    assert_eq!(failures, 0, "decode all, errors: {}", failures);
}

/// Test that codepoints beyond U+10FFFF are rejected
fn test_out_of_range() {
    let mut failures = 0;
    let mut buf = [0u8; 8];
    for i in 0x110000..0x1FFFFF {
        let len = utf8_encode(&mut buf, i);
        if len == 0 { continue; }
        let (c, e, n) = utf8_decode(&buf[..len]);
        if !e {
            failures += 1;
        }
        if n != 4 {
            failures += 1;
        }
        let _ = c;
    }
    assert_eq!(failures, 0, "out of range, errors: {}", failures);
}

/// Test that all surrogate halves are rejected
fn test_surrogate_halves() {
    let mut failures = 0;
    let mut buf = [0u8; 8];
    for i in 0xD800..=0xDFFF {
        let len = utf8_encode(&mut buf, i);
        if len == 0 { continue; }
        let (c, e, _n) = utf8_decode(&buf[..len]);
        if !e {
            failures += 1;
        }
        let _ = c;
    }
    assert_eq!(failures, 0, "surrogate halves, errors: {}", failures);
}

/// Test non-canonical (overlong) encodings
fn test_noncanonical() {
    let mut buf2 = [0xC0, 0xA4, 0, 0, 0, 0, 0, 0]; // overlong 2-byte
    let (c2, e2, n2) = utf8_decode(&buf2[..2]);
    assert!(e2, "non-canonical len 2, 0x02");
    assert_eq!(n2, 2, "non-canonical recover 2, U+{:04X}", c2);

    let mut buf3 = [0xE0, 0x80, 0xA4, 0, 0, 0, 0, 0];
    let (c3, e3, n3) = utf8_decode(&buf3[..3]);
    assert!(e3, "non-canonical len 3, 0x03");
    assert_eq!(n3, 3, "non-canonical recover 3, U+{:04X}", c3);

    let mut buf4 = [0xF0, 0x80, 0x80, 0xA4, 0, 0, 0, 0];
    let (c4, e4, n4) = utf8_decode(&buf4[..4]);
    assert!(e4, "non-canonical encoding len 4, 0x04");
    assert_eq!(n4, 4, "non-canonical recover 4, U+{:04X}", c4);
}

/// Test invalid byte sequences (~bogus bytes)
fn test_bogus_bytes() {
    // Invalid first byte: 0xff
    let buf0 = [0xffu8, 0, 0, 0];
    let (c0, e0, n0) = utf8_decode(&buf0[..1]);
    assert!(e0, "bogus [ff] 0x{:02x} U+{:04X}", e0 as u8, c0);
    assert_eq!(n0, 1, "bogus [ff] recovery {}", n0);

    // Invalid first byte: 0x80
    let buf1 = [0x80u8, 0, 0, 0];
    let (c1, e1, n1) = utf8_decode(&buf1[..1]);
    assert!(e1, "bogus [80] 0x{:02x} U+{:04X}", e1 as u8, c1);
    assert_eq!(n1, 1, "bogus [80] recovery {}", n1);

    // Two-byte start, wrong second byte
    let buf2 = [0xC0u8, 0x0A, 0, 0];
    let (c2, e2, n2) = utf8_decode(&buf2[..2]);
    assert!(e2, "bogus [c0 0a] 0x{:02x} U+{:04X}", e2 as u8, c2);
    assert_eq!(n2, 2, "bogus [c0 0a] recovery {}", n2);
}

#[test]
fn test_original_suite() {
    test_decode_all();
    test_out_of_range();
    test_surrogate_halves();
    test_noncanonical();
    test_bogus_bytes();
}