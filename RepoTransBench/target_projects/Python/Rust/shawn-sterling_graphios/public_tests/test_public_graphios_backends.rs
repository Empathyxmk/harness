use graphios_backends::*;

#[test]
fn test_public_strip_forbidden_chars() {
    assert_eq!(strip_forbidden_chars("a/b:c*d?e<f>g|h"), "abcdefg");
}

#[test]
fn test_public_strip_and_lower() {
    assert_eq!(strip_and_lower("AbC-DeF_123"), "abc-def_123");
}

#[test]
fn test_public_string_cleanup() {
    assert_eq!(string_cleanup("   Remove   Spaces   "), "Remove Spaces");
}

#[test]
fn test_public_string_cleanup_replaces() {
    assert_eq!(string_cleanup("strip\tit   now"), "strip it now");
}

#[test]
fn test_public_camel_case_to_underscore() {
    assert_eq!(camel_case_to_underscore("PublicCaseToUnderscore"), "public_case_to_underscore");
}

#[test]
fn test_public_strip_unicode() {
    let text = "café 漢字";
    let result = strip_unicode(text);
    assert!(result.contains("cafe"));
    assert!(result.chars().all(|c| (c as u32) < 128));
}

#[test]
fn test_public_getattr_from_path() {
    let res = getattr_from_path("dummy_mod.Dummy.Inner.value");
    assert_eq!(res, 404);
}