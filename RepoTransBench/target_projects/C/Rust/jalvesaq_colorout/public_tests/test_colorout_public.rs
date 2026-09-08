use jalvesaq_colorout::{is_word_fn, is_string_number};

#[test]
fn test_isword_public_fn() {
    // Different from private: test values with public data
    assert_eq!(is_word_fn("hello123"), true);
    assert_eq!(is_word_fn("_alpha"), true);
    assert_eq!(is_word_fn("..beta"), true);
    // Change: use symbols as non-words
    assert_eq!(is_word_fn("?h"), false);
    assert_eq!(is_word_fn("!@#"), false);
}

#[test]
fn test_isword_edge_cases_public_fn() {
    // Special cases: numbers, symbols, single-dot, public set
    assert_eq!(is_word_fn("1234"), false);           // all digit
    assert_eq!(is_word_fn("_"), true);               // single underscore
    assert_eq!(is_word_fn("."), true);               // single dot
    assert_eq!(is_word_fn("6e4"), false);            // "6e4" not treated as word (digit start)
}

#[test]
fn test_isstringnumber_public_fn() {
    // Different numbers than private test
    assert_eq!(is_string_number("12345"), true);    // simple integer
    assert_eq!(is_string_number("-9876"), true);    // negative
    assert_eq!(is_string_number("+555"), true);     // positive sign
    assert_eq!(is_string_number("007"), true);      // leading zeros
    assert_eq!(is_string_number("12a34"), false);   // alpha inside
    assert_eq!(is_string_number("abc"), false);     // not a number
}

#[test]
fn test_isstringnumber_edge_cases_public_fn() {
    // Public, different edge cases
    assert_eq!(is_string_number(""), false);           // empty string
    assert_eq!(is_string_number("+"), false);          // just sign, no digits
    assert_eq!(is_string_number("-"), false);          // just sign, no digits
    assert_eq!(is_string_number("--100"), false);      // double sign, invalid
    assert_eq!(is_string_number("9-3"), false);        // sign in wrong place
}