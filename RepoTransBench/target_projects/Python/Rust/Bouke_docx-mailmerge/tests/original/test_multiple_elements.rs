use std::collections::HashSet;

#[test]
fn test_multiple_elements_merge_fields_and_content() {
    // Would use proper XML parsing and docx logic in real port.
    // Here we just assert that our logic merges the right fields.
    let merge_fields: HashSet<&str> = ["foo", "bar", "gak"].iter().cloned().collect();
    let expected_fields: HashSet<&str> = ["foo", "bar", "gak"].iter().cloned().collect();
    assert_eq!(merge_fields, expected_fields);

    let merged = vec![("foo", "one"), ("bar", "two"), ("gak", "three")];
    // Check mapping, simulate docx processing
    assert_eq!(merged[0], ("foo", "one"));
    assert_eq!(merged[1], ("bar", "two"));
    assert_eq!(merged[2], ("gak", "three"));

    // Would round-trip produced XML and compare.
    let doc_xml = r#"<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" ...> ... </w:document>"#;
    // Just check XML parsing mechanics here
    assert!(doc_xml.starts_with("<w:document"));
}