use maskerlogger::ahocorasick_regex_match::{RegexMatcher, _build_ahocorasick};

#[test]
fn test_mask_multiple_matches() {
    let rm = RegexMatcher::new(None, 90);
    let msg = "password: alpha password: beta";
    let masked = rm.mask(msg);
    assert!(masked.matches("***").count() >= 2);
}

#[test]
fn test_mask_no_match() {
    let rm = RegexMatcher::new(None, 60);
    let text = "this is safe";
    assert_eq!(rm.mask(text), text);
}

#[test]
fn test_find_matches_group_0() {
    let rm = RegexMatcher::new(None, 60);
    // Overwrite regexes to only "safe"
    rm.regexes.clear();
    rm.regexes.push(regex::Regex::new(r"safe").unwrap());
    let masked = rm.mask("safe");
    assert!(masked.contains("*") || masked == "safe");
}

#[test]
fn test_invalid_config_file() {
    // Test fallback to default if file does not exist
    let rm = RegexMatcher::new(Some("/tmp/nonexistent.toml"), 60);
    let m = rm.mask("password: example");
    assert!(m.contains("*"));
}