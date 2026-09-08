// Translated from NormalizationTest.txt (Part 1/84)
// Unicode Normalization Test Suite 15.1.0
// Source: https://www.unicode.org/Public/UNIDATA/NormalizationTest.txt
// Test logic: For each line, test that the normalization invariants hold.

extern crate unicode_normalization;

use unicode_normalization::{is_nfc, is_nfkc, is_nfd, is_nfkd, UnicodeNormalization};

/// Parse a string of space-separated hex codepoints into a String
fn codepoints_to_string(s: &str) -> String {
    let chars: Vec<char> = s
        .split_whitespace()
        .filter_map(|h| u32::from_str_radix(h, 16).ok())
        .filter_map(std::char::from_u32)
        .collect();
    chars.iter().collect()
}

/// Run normalization suite for a single test tuple (c1; c2; c3; c4; c5)
fn test_normalization_line(c1: &str, c2: &str, c3: &str, c4: &str, c5: &str) {
    let s1 = codepoints_to_string(c1);
    let s2 = codepoints_to_string(c2);
    let s3 = codepoints_to_string(c3);
    let s4 = codepoints_to_string(c4);
    let s5 = codepoints_to_string(c5);

    // NFC
    assert_eq!(s2, s1.nfc().collect::<String>(), "NFC(c1) != c2; c1 = {c1}");
    assert_eq!(s2, s2.nfc().collect::<String>(), "NFC(c2) != c2; c2 = {c2}");
    assert_eq!(s2, s3.nfc().collect::<String>(), "NFC(c3) != c2; c3 = {c3}");
    assert_eq!(s4, s4.nfc().collect::<String>(), "NFC(c4) != c4; c4 = {c4}");
    assert_eq!(s4, s5.nfc().collect::<String>(), "NFC(c5) != c4; c5 = {c5}");

    // NFD
    assert_eq!(s3, s1.nfd().collect::<String>(), "NFD(c1) != c3; c1 = {c1}");
    assert_eq!(s3, s2.nfd().collect::<String>(), "NFD(c2) != c3; c2 = {c2}");
    assert_eq!(s3, s3.nfd().collect::<String>(), "NFD(c3) != c3; c3 = {c3}");
    assert_eq!(s5, s4.nfd().collect::<String>(), "NFD(c4) != c5; c4 = {c4}");
    assert_eq!(s5, s5.nfd().collect::<String>(), "NFD(c5) != c5; c5 = {c5}");

    // NFKC
    assert_eq!(s4, s1.nfkc().collect::<String>(), "NFKC(c1) != c4; c1 = {c1}");
    assert_eq!(s4, s2.nfkc().collect::<String>(), "NFKC(c2) != c4; c2 = {c2}");
    assert_eq!(s4, s3.nfkc().collect::<String>(), "NFKC(c3) != c4; c3 = {c3}");
    assert_eq!(s4, s4.nfkc().collect::<String>(), "NFKC(c4) != c4; c4 = {c4}");
    assert_eq!(s4, s5.nfkc().collect::<String>(), "NFKC(c5) != c4; c5 = {c5}");

    // NFKD
    assert_eq!(s5, s1.nfkd().collect::<String>(), "NFKD(c1) != c5; c1 = {c1}");
    assert_eq!(s5, s2.nfkd().collect::<String>(), "NFKD(c2) != c5; c2 = {c2}");
    assert_eq!(s5, s3.nfkd().collect::<String>(), "NFKD(c3) != c5; c3 = {c3}");
    assert_eq!(s5, s4.nfkd().collect::<String>(), "NFKD(c4) != c5; c4 = {c4}");
    assert_eq!(s5, s5.nfkd().collect::<String>(), "NFKD(c5) != c5; c5 = {c5}");
}

#[test]
fn normalization_test_part1() {
    let data = [
        // Format: c1; c2; c3; c4; c5;
        ("1E0A",          "1E0A",          "0044 0307",          "1E0A",          "0044 0307"),
        ("1E0C",          "1E0C",          "0044 0323",          "1E0C",          "0044 0323"),
        ("1E0A 0323",     "1E0C 0307",     "0044 0323 0307",     "1E0C 0307",     "0044 0323 0307"),
        ("1E0C 0307",     "1E0C 0307",     "0044 0323 0307",     "1E0C 0307",     "0044 0323 0307"),
        ("0044 0307 0323","1E0C 0307",     "0044 0323 0307",     "1E0C 0307",     "0044 0323 0307"),
        ("0044 0323 0307","1E0C 0307",     "0044 0323 0307",     "1E0C 0307",     "0044 0323 0307"),
        ("1E0A 031B",     "1E0A 031B",     "0044 031B 0307",     "1E0A 031B",     "0044 031B 0307"),
        ("1E0C 031B",     "1E0C 031B",     "0044 031B 0323",     "1E0C 031B",     "0044 031B 0323"),
        ("1E0A 031B 0323","1E0C 031B 0307","0044 031B 0323 0307","1E0C 031B 0307","0044 031B 0323 0307"),
        ("1E0C 031B 0307","1E0C 031B 0307","0044 031B 0323 0307","1E0C 031B 0307","0044 031B 0323 0307"),
        ("0044 031B 0307 0323","1E0C 031B 0307","0044 031B 0323 0307","1E0C 031B 0307","0044 031B 0323 0307"),
        ("0044 031B 0323 0307","1E0C 031B 0307","0044 031B 0323 0307","1E0C 031B 0307","0044 031B 0323 0307"),
        ("00C8",          "00C8",          "0045 0300",          "00C8",          "0045 0300"),
        ("0112",          "0112",          "0045 0304",          "0112",          "0045 0304"),
        ("0045 0300",     "00C8",          "0045 0300",          "00C8",          "0045 0300"),
        ("0045 0304",     "0112",          "0045 0304",          "0112",          "0045 0304"),
        ("1E14",          "1E14",          "0045 0304 0300",     "1E14",          "0045 0304 0300"),
        ("0112 0300",     "1E14",          "0045 0304 0300",     "1E14",          "0045 0304 0300"),
        ("1E14 0304",     "1E14 0304",     "0045 0304 0300 0304","1E14 0304",     "0045 0304 0300 0304"),
        ("0045 0304 0300","1E14",          "0045 0304 0300",     "1E14",          "0045 0304 0300"),
        ("0045 0300 0304","00C8 0304",     "0045 0300 0304",     "00C8 0304",     "0045 0300 0304"),
        ("05B8 05B9 05B1 0591 05C3 05B0 05AC 059F","05B1 05B8 05B9 0591 05C3 05B0 05AC 059F",
            "05B1 05B8 05B9 0591 05C3 05B0 05AC 059F","05B1 05B8 05B9 0591 05C3 05B0 05AC 059F","05B1 05B8 05B9 0591 05C3 05B0 05AC 059F"),
        ("0592 05B7 05BC 05A5 05B0 05C0 05C4 05AD","05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4",
            "05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4","05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4","05B0 05B7 05BC 05A5 0592 05C0 05AD 05C4"),
        ("1100 AC00 11A8", "1100 AC01","1100 1100 1161 11A8", "1100 AC01", "1100 1100 1161 11A8"),
        ("1100 AC00 11A8 11A8","1100 AC01 11A8","1100 1100 1161 11A8 11A8","1100 AC01 11A8","1100 1100 1161 11A8 11A8"),
        // Part 1 character by character (first 50 or so lines)
        ("00A0", "00A0", "00A0", "0020", "0020"),
        ("00A8", "00A8", "00A8", "0020 0308", "0020 0308"),
        ("00AA", "00AA", "00AA", "0061", "0061"),
        ("00AF", "00AF", "00AF", "0020 0304", "0020 0304"),
        ("00B2", "00B2", "00B2", "0032", "0032"),
        ("00B3", "00B3", "00B3", "0033", "0033"),
        ("00B4", "00B4", "00B4", "0020 0301", "0020 0301"),
        ("00B5", "00B5", "00B5", "03BC", "03BC"),
        ("00B8", "00B8", "00B8", "0020 0327", "0020 0327"),
        ("00B9", "00B9", "00B9", "0031", "0031"),
        ("00BA", "00BA", "00BA", "006F", "006F"),
        ("00BC", "00BC", "00BC", "0031 2044 0034", "0031 2044 0034"),
        ("00BD", "00BD", "00BD", "0031 2044 0032", "0031 2044 0032"),
        ("00BE", "00BE", "00BE", "0033 2044 0034", "0033 2044 0034"),
        ("00C0", "00C0", "0041 0300", "00C0", "0041 0300"),
        ("00C1", "00C1", "0041 0301", "00C1", "0041 0301"),
        ("00C2", "00C2", "0041 0302", "00C2", "0041 0302"),
        ("00C3", "00C3", "0041 0303", "00C3", "0041 0303"),
        ("00C4", "00C4", "0041 0308", "00C4", "0041 0308"),
        ("00C5", "00C5", "0041 030A", "00C5", "0041 030A"),
        ("00C7", "00C7", "0043 0327", "00C7", "0043 0327"),
        ("00C8", "00C8", "0045 0300", "00C8", "0045 0300"),
        ("00C9", "00C9", "0045 0301", "00C9", "0045 0301"),
        ("00CA", "00CA", "0045 0302", "00CA", "0045 0302"),
        ("00CB", "00CB", "0045 0308", "00CB", "0045 0308"),
        ("00CC", "00CC", "0049 0300", "00CC", "0049 0300"),
        ("00CD", "00CD", "0049 0301", "00CD", "0049 0301"),
        ("00CE", "00CE", "0049 0302", "00CE", "0049 0302"),
        ("00CF", "00CF", "0049 0308", "00CF", "0049 0308"),
        ("00D1", "00D1", "004E 0303", "00D1", "004E 0303"),
        ("00D2", "00D2", "004F 0300", "00D2", "004F 0300"),
        ("00D3", "00D3", "004F 0301", "00D3", "004F 0301"),
        ("00D4", "00D4", "004F 0302", "00D4", "004F 0302"),
        ("00D5", "00D5", "004F 0303", "00D5", "004F 0303"),
        ("00D6", "00D6", "004F 0308", "00D6", "004F 0308"),
        ("00D9", "00D9", "0055 0300", "00D9", "0055 0300"),
        ("00DA", "00DA", "0055 0301", "00DA", "0055 0301"),
        ("00DB", "00DB", "0055 0302", "00DB", "0055 0302"),
        ("00DC", "00DC", "0055 0308", "00DC", "0055 0308"),
        ("00DD", "00DD", "0059 0301", "00DD", "0059 0301"),
        ("00E0", "00E0", "0061 0300", "00E0", "0061 0300"),
        ("00E1", "00E1", "0061 0301", "00E1", "0061 0301"),
        ("00E2", "00E2", "0061 0302", "00E2", "0061 0302"),
        ("00E3", "00E3", "0061 0303", "00E3", "0061 0303"),
        ("00E4", "00E4", "0061 0308", "00E4", "0061 0308"),
        ("00E5", "00E5", "0061 030A", "00E5", "0061 030A"),
        ("00E7", "00E7", "0063 0327", "00E7", "0063 0327"),
    ];
    for (c1, c2, c3, c4, c5) in data {
        test_normalization_line(c1, c2, c3, c4, c5);
    }
}