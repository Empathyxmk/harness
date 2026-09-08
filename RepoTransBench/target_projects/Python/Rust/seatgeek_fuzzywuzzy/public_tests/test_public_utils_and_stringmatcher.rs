use seatgeek_fuzzywuzzy::utils;
use seatgeek_fuzzywuzzy::string_matcher::StringMatcher;

#[test]
fn test_asciidammit_public() {
    let s = "Café Noël Über ß";
    let result = utils::asciidammit(s);
    assert!(result.is_ascii());
    assert!(!result.contains('\u{e9}')); // 'é' replaced
}

#[test]
fn test_asciionly_public() {
    let s = utils::asciidammit("façade naïve jalapeño");
    let result = utils::asciionly(&s);
    for c in result.chars() {
        assert!(c.is_ascii_alphanumeric() || c == ' ');
    }
}

#[test]
fn test_full_process_public() {
    let s = "Fußball & Crème brûlée";
    let result = utils::full_process(s, false);
    assert!(result.is_ascii()); // basic logic
    assert!(!result.contains("&"));
}

#[test]
fn test_stringmatcher_ratio_public() {
    let s1 = "hello";
    let s2 = "hullo";
    let mut m = StringMatcher::new();
    m.set_seq1(s1);
    m.set_seq2(s2);
    let ratio = m.ratio();
    assert!(ratio > 0.7 && ratio < 1.0);
}