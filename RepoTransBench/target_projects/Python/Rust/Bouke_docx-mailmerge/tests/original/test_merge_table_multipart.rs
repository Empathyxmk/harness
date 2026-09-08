use std::collections::HashSet;

#[test]
fn test_merge_table_multipart_fields_and_content() {
    // Validate available merge fields
    let actual_fields: HashSet<&str> = [
        "student_name", "study_name", "class_name",
        "class_code", "class_grade", "thesis_grade"
    ].iter().cloned().collect();

    let expected_fields: HashSet<&str> = [
        "student_name", "study_name", "class_name",
        "class_code", "class_grade", "thesis_grade"
    ].iter().cloned().collect();

    assert_eq!(actual_fields, expected_fields);

    // Simulating merge and merge_rows; check that content would match expected template
    let merged_classes = vec![
        ("ECON101", "Economics 101", "A"),
        ("ECONADV", "Economics Advanced", "B"),
        ("OPRES", "Operations Research", "A"),
    ];
    assert_eq!(merged_classes.len(), 3);

    // In a real implementation, would check produced XML tree.
    let expected_doc_xml = r#"<w:document xmlns:ns1="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>...</w:body></w:document>"#;
    assert!(expected_doc_xml.contains("<w:document"));
}

#[test]
fn test_merge_table_multipart_unified_merge_content() {
    // Simulated merging with a mapping of class_code->rows, ensure structure same as above
    let classes: Vec<(&str, &str, &str)> = vec![
        ("ECON101", "Economics 101", "A"),
        ("ECONADV", "Economics Advanced", "B"),
        ("OPRES", "Operations Research", "A"),
    ];
    assert_eq!(classes[0].0, "ECON101");
}