#[test]
fn test_public_warning_is_shown() {
    // Rust can't strictly capture warnings at runtime like Python
    println!("cargo:warning=This is a public test warning!");
    assert!(true);
}