// Translated from public_tests/test_files_public.py

#[test]
fn test_tag_public() {
    let url = "/public/sample.jpeg";
    let tag = format!(r#"<img alt="" height="80" src="{}" width="120" />"#, url);
    assert!(tag.contains("height=\"80\""));
    assert!(tag.contains("width=\"120\""));
}

#[test]
fn test_extensions_public() {
    let name = "remote_public_sample.jpeg.18x18_q85.bmp";
    assert_eq!(std::path::Path::new(name).extension().unwrap(), "bmp");
}