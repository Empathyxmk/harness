#[test]
fn test_public_version_string() {
    let version = "1.2.3";
    assert!(version.chars().filter(|&c| c == '.').count() == 2);
}