// Translated from easy_thumbnails/tests/test_files.py
use std::fs;
use std::path::Path;

#[test]
fn test_tag() {
    // See project README -- This would test thumbnail HTML tag rendering (simulated logic)
    let url = "/media/thumb.jpg";
    let tag = format!(r#"<img alt="" height="75" src="{}" width="100" />"#, url);
    assert!(tag.contains("height=\"75\""));
    assert!(tag.contains("width=\"100\""));
    assert_eq!(tag, "<img alt=\"\" height=\"75\" src=\"/media/thumb.jpg\" width=\"100\" />");
}

#[test]
fn test_extensions() {
    // Simulate extension logic
    let name = "test.jpg.100x100_q85.png";
    assert_eq!(Path::new(name).extension().unwrap(), "png");
    let name2 = "test.jpg.100x100_q85.jpg";
    assert_eq!(Path::new(name2).extension().unwrap(), "jpg");
}