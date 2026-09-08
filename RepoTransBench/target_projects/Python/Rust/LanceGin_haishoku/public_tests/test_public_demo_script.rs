use std::path::Path;

#[test]
fn test_demo_png_exists() {
    assert!(Path::new("demo/demo_01.png").exists());
}