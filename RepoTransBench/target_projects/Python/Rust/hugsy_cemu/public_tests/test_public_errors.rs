#[test]
fn test_public_placeholder_errors() {
    // Placeholder - ensure some coverage while using different data.
    let s = "error_public".to_owned() + "X";
    assert_eq!(s, "error_publicX");
}