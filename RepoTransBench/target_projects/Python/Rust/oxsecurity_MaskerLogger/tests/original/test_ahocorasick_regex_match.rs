use maskerlogger::ahocorasick_regex_match::RegexMatcher;

#[test]
fn test_find_matches_and_mask() {
    let matcher = RegexMatcher::new(None, 90);
    let msg = "password: hunter2";
    let matches = matcher.find_matches(msg);
    assert!(!matches.is_empty());
    let masked = matcher.mask(msg);
    assert!(masked.contains("***"));
}

#[test]
fn test_parse_config_failure() {
    let matcher = RegexMatcher::new(Some("nonexistent_path.toml"), 80);
    let out = matcher.mask("password: hunter2 super");
    assert!(out.contains("*"));
}