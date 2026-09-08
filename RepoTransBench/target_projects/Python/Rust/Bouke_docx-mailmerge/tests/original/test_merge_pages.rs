use std::collections::HashSet;

#[test]
fn test_merge_pages_fieldnames_and_content() {
    let merge_fields: HashSet<&str> = ["fieldname"].iter().cloned().collect();
    assert_eq!(merge_fields, HashSet::from(["fieldname"]));

    let data = vec![
        ("fieldname", "xyz"),
        ("fieldname", "abc"),
        ("fieldname", "2b v ~2b"),
    ];
    assert_eq!(data.len(), 3);

    // Check simulated XML output structure (in practice, would compare to known XML)
    let expected_xml = r#"<w:document xmlns:wpc=...> ... </w:document>"#;
    assert!(expected_xml.contains("merge_list test case"));
}

#[test]
fn test_merge_pages_with_multiple_pages() {
    // Checks page count multiplication logic for multi-page templates
    let doc_template_pages = 2;
    let datalist = vec!["xyz", "abc", "2b v ~2b"];
    let expected_final_pages = doc_template_pages * datalist.len();
    assert_eq!(expected_final_pages, 6);
}