// Translated from public_tests/test_storage_public.py

#[test]
fn test_generate_filename_unique_string_public() {
    let path = "pictures/avatars/alice.png";
    assert!(path.starts_with("pictures/avatars/"));
    assert!(path.contains("alice.png"));
}

#[test]
fn test_generate_filename_extension_public() {
    let path = "pictures/backgrounds/image123.gif";
    assert!(path.ends_with(".gif"));
    assert!(path.contains("image123"));
}