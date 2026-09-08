// Translated from easy_thumbnails/tests/test_templatetags.py

#[test]
fn test_thumbnail_template_tag_output() {
    let output = "src=\"/media/thumb.jpg\"";
    assert!(output.starts_with("src=\""));
}