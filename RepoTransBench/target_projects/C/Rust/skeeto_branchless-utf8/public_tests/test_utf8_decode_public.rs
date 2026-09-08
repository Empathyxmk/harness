// Translation of test/test_utf8_decode_public.c from C to Rust.

use skeeto_branchless_utf8::utf8_decode;

macro_rules! assert_ex {
    ($expr:expr) => {
        if !$expr {
            panic!("ASSERTION FAILED: {} at {}:{}", stringify!($expr), file!(), line!());
        }
    };
}

#[test]
fn test_utf8_decode_public() {
    // ASCII: 'z'
    let b1 = [0x7A, 0x00];
    let (c, e, _) = utf8_decode(&b1[..1]);
    assert_ex!(c == 0x7A && !e);

    // Two-byte: U+00A9
    let b2 = [0xC2, 0xA9, 0x00];
    let (c, e, _) = utf8_decode(&b2[..2]);
    assert_ex!(c == 0xA9 && !e);

    // Three-byte: U+20AC
    let b3 = [0xE2, 0x82, 0xAC, 0x00];
    let (c, e, _) = utf8_decode(&b3[..3]);
    assert_ex!(c == 0x20AC && !e);

    // Four-byte: U+1F680
    let b4 = [0xF0, 0x9F, 0x9A, 0x80, 0x00];
    let (c, e, _) = utf8_decode(&b4[..4]);
    assert_ex!(c == 0x1F680 && !e);

    // Overlong 2-byte (U+0000 as 2 bytes)
    let overlong2 = [0xC0, 0x80, 0x00];
    let (c, e, _) = utf8_decode(&overlong2[..2]);
    let _ = c;
    assert_ex!(e);

    // Overlong 3-byte (U+0000 as 3 bytes)
    let overlong3 = [0xE0, 0x80, 0x80, 0x00];
    let (c, e, _) = utf8_decode(&overlong3[..3]);
    let _ = c;
    assert_ex!(e);

    // Invalid first byte
    let inv1 = [0xFF, 0x00];
    let (c, e, _) = utf8_decode(&inv1[..1]);
    let _ = c;
    assert_ex!(e);

    // Valid 2-byte: U+07FF
    let max2 = [0xDF, 0xBF, 0x00];
    let (c, e, _) = utf8_decode(&max2[..2]);
    assert_ex!(c == 0x7FF && !e);

    // Valid 3-byte: U+FFFF
    let max3 = [0xEF, 0xBF, 0xBF, 0x00];
    let (c, e, _) = utf8_decode(&max3[..3]);
    assert_ex!(c == 0xFFFF && !e);

    // Out of range: U+110000 (invalid)
    let oor = [0xF4, 0x90, 0x80, 0x80, 0x00];
    let (c, e, _) = utf8_decode(&oor[..4]);
    let _ = c;
    assert_ex!(e);

    // Surrogate: U+DFFF
    let surrogate = [0xED, 0xBF, 0xBF, 0x00];
    let (c, e, _) = utf8_decode(&surrogate[..3]);
    let _ = c;
    assert_ex!(e);
}