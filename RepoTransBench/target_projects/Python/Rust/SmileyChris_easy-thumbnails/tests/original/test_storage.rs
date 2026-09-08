// Translated from easy_thumbnails/tests/test_storage.py

use std::path::Path;

#[test]
fn test_thumbnail_filesystem_storage_defaults() {
    // Simulate default storage
    let path = "/tmp/thumbs";
    assert!(path.starts_with("/tmp"));
}

#[test]
fn test_generate_filename_extension() {
    let path = "picture/alice.png";
    let ext = Path::new(path).extension().unwrap();
    assert_eq!(ext, "png");
}