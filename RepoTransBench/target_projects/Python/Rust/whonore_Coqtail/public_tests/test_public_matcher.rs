use coqtail::matcher::*;

#[test]
fn test_public_match_tokens_diff() {
    let pattern = ["cat", "dog"];
    let text = ["cat", "bird"];
    let output = match_tokens(&pattern, &text);
    assert!(!output);
}

#[test]
fn test_public_match_tokens_contained() {
    let pattern = ["tree", "leaf"];
    let text = ["tree", "root", "leaf"];
    let output = match_tokens(&pattern, &text[0..2]) || match_tokens(&pattern, &text[1..3]);
    assert!(output || match_tokens(&pattern, &text[1..3]));
}

#[test]
fn test_public_match_tokens_success() {
    let pattern = ["sun", "light"];
    let text = ["sun", "light"];
    let output = match_tokens(&pattern, &text);
    assert!(output);
}

#[test]
fn test_public_match_tokens_too_long() {
    let pattern = ["alpha", "beta", "gamma"];
    let text = ["alpha", "beta", "gamma", "delta"];
    let output = match_tokens(&pattern, &text);
    assert!(!output);
}

#[test]
fn test_public_match_tokens_empty_pattern() {
    let pattern: [&str; 0] = [];
    let text = ["x", "y", "z"];
    let output = match_tokens(&pattern, &text);
    assert!(output);
}