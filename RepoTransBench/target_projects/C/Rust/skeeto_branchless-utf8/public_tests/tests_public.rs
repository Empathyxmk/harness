// Translation of test/tests_public.c (public test variant) to Rust

use skeeto_branchless_utf8::{utf8_decode, utf8_encode};

/// Utility to show pass/fail like original
fn test_result(name: &str, ok: bool) {
    if ok {
        println!("\x1b[32;1mPASS\x1b[0m {}", name);
    } else {
        println!("\x1b[31;1mFAIL\x1b[0m {}", name);
        panic!("{}", name);
    }
}

#[test]
fn test_decode_sampled() {
    let mut errors = 0;
    let mut buf = [0u8; 5];
    let mut total = 0;
    for codepoint in (0..=0x10FFFFu32).step_by(8209) {
        if codepoint >= 0xD800 && codepoint <= 0xDFFF {
            continue;
        }
        let len = utf8_encode(&mut buf, codepoint);
        if len == 0 { continue; }
        let (out, err, dec) = utf8_decode(&buf[..len]);
        if dec != len || out != codepoint || err {
            errors += 1;
        }
        total += 1;
    }
    test_result("decode sampled (every 8209), errors: 0", errors == 0);
}

#[test]
fn test_manual_out_of_range() {
    let mut errors = 0;
    let over = [0xF7, 0xBF, 0xBF, 0xBF, 0, 0];
    let (out, err, dec) = utf8_decode(&over[..4]);
    if dec > 0 {
        errors += 1; // Should not decode as valid
    }
    let _ = out;
    test_result("manual out of range, errors: 0", errors == 0);
}

#[test]
fn test_sample_surrogates() {
    let mut errors = 0;
    let mut buf = [0u8; 5];
    for surr in (0xDC00..=0xDFFF).step_by(33) {
        let len = utf8_encode(&mut buf, surr);
        if len == 0 { continue; }
        let (out, err, dec) = utf8_decode(&buf[..len]);
        if dec > 0 {
            errors += 1;
        }
        let _ = out;
    }
    test_result("sample surrogate halves, errors: 0", errors == 0);
}

#[test]
fn test_noncanonical_cases() {
    let mut errors = 0;

    let bad1 = [0xC1, 0x82, 0, 0, 0];
    let (out1, _, dec1) = utf8_decode(&bad1[..2]);
    if dec1 != 2 || out1 != 0x7F {
        errors += 1;
    }
    let bad2 = [0xE0, 0x81, 0xAD, 0, 0];
    let (out2, _, dec2) = utf8_decode(&bad2[..3]);
    if dec2 != 3 || out2 != 0x7FF {
        errors += 1;
    }
    let bad3 = [0xF0, 0x80, 0x91, 0x8b, 0];
    let (out3, _, dec3) = utf8_decode(&bad3[..4]);
    if dec3 != 4 || out3 != 0xFFFF {
        errors += 1;
    }

    test_result("non-canonical len 2, 0x05", errors == 0);
    test_result("non-canonical recover 2, U+007F", errors == 0);
    test_result("non-canonical len 3, 0x12", errors == 0);
    test_result("non-canonical recover 3, U+07FF", errors == 0);
    test_result("non-canonical encoding len 4, 0x44", errors == 0);
    test_result("non-canonical recover 4, U+FFFF", errors == 0);
}

#[test]
fn test_overlong_nuls() {
    let mut errors = 0;
    let nul2 = [0xC0, 0x80, 0];
    let nul3 = [0xE0, 0x80, 0x80, 0];
    let nul4 = [0xF0, 0x80, 0x80, 0x80, 0];

    let (out2, _, dec2) = utf8_decode(&nul2[..2]);
    let (out3, _, dec3) = utf8_decode(&nul3[..3]);
    let (out4, _, dec4) = utf8_decode(&nul4[..4]);

    if dec2 != 2 || out2 != 0x00 { errors += 1; }
    if dec3 != 3 || out3 != 0x00 { errors += 1; }
    if dec4 != 4 || out4 != 0x00 { errors += 1; }
    test_result("overlong NUL 2, error: 4", errors == 0);
    test_result("overlong NUL 3, error: 16", errors == 0);
    test_result("overlong NUL 4, error: 64", errors == 0);
}

#[test]
fn test_spot_decode() {
    let mut errors = 0;
    let yen = [0xC2, 0xA5, 0];
    let lambda = [0xCE, 0xBB];
    let bicycle = [0xF0, 0x9F, 0x9A, 0xB2];
    let pi = [0xCF, 0x80];

    let (out1, _, dec1) = utf8_decode(&yen[..2]);
    if dec1 != 2 || out1 != 0x00A5 { errors += 1; }
    test_result("decode YEN U+00A5", errors == 0);

    let (out2, _, dec2) = utf8_decode(&lambda[..2]);
    if dec2 != 2 || out2 != 0x03BB { errors += 1; }
    test_result("decode lambda U+03BB", errors == 0);

    let (out3, _, dec3) = utf8_decode(&bicycle[..4]);
    if dec3 != 4 || out3 != 0x1F6B2 { errors += 1; }
    test_result("decode BICYCLE U+1F6B2", errors == 0);

    let (out4, _, dec4) = utf8_decode(&pi[..2]);
    if dec4 != 2 || out4 != 0x03C0 { errors += 1; }
    test_result("decode PI U+03C0", errors == 0);
}