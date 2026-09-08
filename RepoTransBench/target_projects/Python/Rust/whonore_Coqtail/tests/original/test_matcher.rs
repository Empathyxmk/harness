use coqtail::matcher::*;

#[test]
fn test_match_tokens_diff() {
    let pattern = ["cat", "dog"];
    let text = ["cat", "bird"];
    let output = match_tokens(&pattern, &text);
    assert!(!output);
}

#[test]
fn test_match_tokens_contained() {
    let pattern = ["tree", "leaf"];
    let text = ["tree", "root", "leaf"];
    let output = match_tokens(&pattern, &text[0..2]) || match_tokens(&pattern, &text[1..3]);
    // Simulate "contained" by trying slices.
    assert!(output || match_tokens(&pattern, &text[1..3]));
}

#[test]
fn test_match_tokens_success() {
    let pattern = ["sun", "light"];
    let text = ["sun", "light"];
    let output = match_tokens(&pattern, &text);
    assert!(output);
}

#[test]
fn test_match_tokens_too_long() {
    let pattern = ["alpha", "beta", "gamma"];
    let text = ["alpha", "beta", "gamma", "delta"];
    let output = match_tokens(&pattern, &text);
    assert!(!output);
}

#[test]
fn test_match_tokens_empty_pattern() {
    let pattern: [&str; 0] = [];
    let text = ["x", "y", "z"];
    let output = match_tokens(&pattern, &text);
    assert!(output);
}

#[test]
fn test_matcher_generate_patterns() {
    // These match only the hardcoded strings for the given slice combos, as in the python matcher tests.
    assert_eq!(matcher(Some((1, 5)), Some((1, 5))), r"\%2l\%>1c\|\%>2l\%<5l\|\%5l\%<6c");
    assert_eq!(matcher(Some((1, 5)), Some((0, 5))), r"\%2l\|\%>2l\%<5l\|\%5l\%<6c");
    assert_eq!(matcher(Some((1, 5)), None), r"\%2l\|\%>2l\%<5l\|\%5l");
    assert_eq!(matcher(Some((1, 2)), Some((1, 5))), r"\%2l\%>1c\%<6c");
    assert_eq!(matcher(Some((1, 2)), None), r"\%2l");
    assert_eq!(matcher(Some((1, 3)), Some((1, 5))), r"\%2l\%>1c\|\%3l\%<6c");
}