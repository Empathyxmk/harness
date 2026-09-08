// Test translated from tests/unit/test_genlz77_public.c

use pfalcon_uzlib::*;

#[test]
fn genlz77_public_pattern_match() {
    // Different input string for LZ77 matching
    let data: [u8; 12] = *b"abcabcabcabc"; // Pattern should produce some LZ77 matches
    let mut m = Lz77Match::default();
    let num = genlz77_find_match(&data, 12, 0, &mut m);
    assert!(num >= 3); // At least 3 matches for repeated "abc" pattern
    // Each match should be of length 3, offset increasing by 3
    assert_eq!(m.len, 3);
    assert_eq!(m.dist, 3);
}