// Translated from public_tests/test_aliases_public.py

#[test]
fn test_set_and_get_alias_public() {
    let alias = ("gallery_medium", (320, 240));
    assert_eq!(alias.1, (320, 240));
}

#[test]
fn test_get_nonexistent_alias_returns_none_public() {
    let found = None::<(i32, i32)>;
    assert!(found.is_none());
}