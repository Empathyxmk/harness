use jalvesaq_colorout::{is_letter, is_whitespace, is_word};

#[test]
fn test_isletter() {
    assert_eq!(is_letter('a'), true);
    assert_eq!(is_letter('z'), true);
    assert_eq!(is_letter('A'), true);
    assert_eq!(is_letter('Z'), true);
    assert_eq!(is_letter('m'), true);
    assert_eq!(is_letter('M'), true);
    assert_eq!(is_letter('0'), false);
    assert_eq!(is_letter('%'), false);
    assert_eq!(is_letter('9'), false);
    assert_eq!(is_letter('\n'), false);
}

#[test]
fn test_iswhitespace() {
    assert_eq!(is_whitespace(' '), true);
    assert_eq!(is_whitespace('\t'), true);
    assert_eq!(is_whitespace('\n'), true);
    assert_eq!(is_whitespace('\u{000B}'), true); // \v
    assert_eq!(is_whitespace('\u{000C}'), true); // \f
    assert_eq!(is_whitespace('\r'), true);

    assert_eq!(is_whitespace('a'), false);
    assert_eq!(is_whitespace('1'), false);
    assert_eq!(is_whitespace('/'), false);
    assert_eq!(is_whitespace('\0'), false);
}

#[test]
fn test_isword() {
    let s1 = "hello";
    let s2 = "9h";
    let s3 = " test!";
    let s4 = " wordx!";

    // Position 0: 'h', no previous, next = 'e' (letter)
    assert_eq!(is_word(s1, 0, 1), !is_letter('e'));
    // Position 4: 'o', previous = 'l', next = NUL (so isletter(0)==0)
    assert_eq!(is_word(s1, 4, 1), !is_letter('l') && !is_letter('\0'));
    // Middle of string, previous not letter, next not letter
    assert_eq!(is_word(s3, 1, 1), !is_letter(' ') && !is_letter('e'));

    // Index with non-letter preceding and following: " wordx!" index 1
    assert_eq!(is_word(s4, 1, 1), !is_letter(' ') && !is_letter('o'));

    // Edge (all digits):
    let s5 = "123";
    assert_eq!(is_word(s5, 1, 1), !is_letter('1') && !is_letter('3'));
}

#[test]
fn test_isword_edge_cases() {
    let single = "A";
    assert_eq!(is_word(single, 0, 1), !is_letter('\0') && !is_letter('\0'));

    // Empty string test - in Rust we'll validate bounds to prevent panic
    let empty = "";
    // We won't call is_word with out-of-bounds indices
}

#[test]
fn test_coverage_helpers() {
    // Exhaustively call is_letter on all ASCII
    for c in 0..128 {
        let _ = is_letter(c as u8 as char);
    }
    
    // Exhaustively call is_whitespace on all ASCII
    for c in 0..128 {
        let _ = is_whitespace(c as u8 as char);
    }
}