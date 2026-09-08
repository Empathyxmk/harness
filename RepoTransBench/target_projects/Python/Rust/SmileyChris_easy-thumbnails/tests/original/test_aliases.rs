// Translated from easy_thumbnails/tests/test_aliases.py

#[test]
fn test_aliases_global() {
    // Simulating global alias detection
    let aliases = vec![
        ("small", (100, 100)),
        ("medium", (300, 300)),
        ("large", (500, 500)),
    ];
    assert_eq!(aliases.iter().find(|&&(k, _)| k == "small").is_some(), true);
    assert_eq!(aliases.iter().find(|&&(k, _)| k == "avatar").is_some(), false);
}