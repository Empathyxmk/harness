use std::fs;
use std::path::Path;

#[test]
fn test_demo_file_exists() {
    let path = Path::new("demo/demo.py");
    assert!(path.exists());
}

#[test]
fn test_demo_png_exists() {
    let path = Path::new("demo/demo_01.png");
    assert!(path.exists());
}