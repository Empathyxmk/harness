use pywizlight_rust::VERSION;

#[test]
fn test_public_version_format() {
    let splits: Vec<&str> = VERSION.split('.').collect();
    assert_eq!(splits.len(), 3);
    for num in &splits {
        assert!(num.chars().all(|c| c.is_digit(10)));
    }
}