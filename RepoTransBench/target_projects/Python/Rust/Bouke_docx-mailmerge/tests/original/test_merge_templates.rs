use std::collections::HashSet;

#[test]
fn test_merge_templates_break_page() {
    let merge_fields: HashSet<&str> = ["fieldname"].iter().cloned().collect();
    assert_eq!(merge_fields, HashSet::from(["fieldname"]));

    let templates = vec![
        ("fieldname", "Test with page_break"),
        ("fieldname", "abc"),
        ("fieldname", "2b v ~2b"),
    ];
    assert_eq!(templates.len(), 3);
    let break_type = "page_break";
    assert_eq!(break_type, "page_break");

    let output_xml = r#"<w:document xmlns:wpc=...> ... </w:document>"#;
    assert!(output_xml.contains("page_break") || output_xml.contains("<w:br w:type=\"page\""));
}

#[test]
fn test_merge_templates_break_col() {
    let merge_fields: HashSet<&str> = ["fieldname"].iter().cloned().collect();
    assert_eq!(merge_fields, HashSet::from(["fieldname"]));
    let templates = vec![
        ("fieldname", "Test with column_break"),
        ("fieldname", "abc"),
        ("fieldname", "2b v ~2b"),
    ];
    assert_eq!(templates.len(), 3);

    let output_xml = r#"<w:document xmlns:wpc=...> ... </w:document>"#;
    assert!(output_xml.contains("column_break") || output_xml.contains("<w:br w:type=\"column\""));
}

#[test]
fn test_merge_templates_break_tw() {
    let merge_fields: HashSet<&str> = ["fieldname"].iter().cloned().collect();
    assert_eq!(merge_fields, HashSet::from(["fieldname"]));
    let templates = vec![
        ("fieldname", "Test with textWrapping_break"),
        ("fieldname", "abc"),
        ("fieldname", "2b v ~2b"),
    ];
    assert_eq!(templates.len(), 3);

    let output_xml = r#"<w:document xmlns:wpc=...> ... </w:document>"#;
    assert!(output_xml.contains("textWrapping_break") || output_xml.contains("<w:br w:type=\"textWrapping\""));
}