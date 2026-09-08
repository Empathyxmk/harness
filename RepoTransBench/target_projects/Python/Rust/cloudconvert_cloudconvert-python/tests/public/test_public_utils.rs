use cloudconvert_cloudconvert_rust::utils;

#[test]
fn test_public_slugify_simple() {
    assert_eq!(utils::slugify("Rust Is Fun!"), "rust-is-fun");
}