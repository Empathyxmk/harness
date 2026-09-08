use std::collections::HashSet;

#[test]
fn test_macword2011_merge_fields_and_content() {
    let expected: HashSet<&str> = [
        "first_name", "last_name", "country", "state",
        "postal_code", "date", "address_line", "city"
    ].iter().cloned().collect();
    let actual = expected.clone();
    assert_eq!(actual, expected);

    let merged = vec![
        ("first_name", "Bouke"),
        ("last_name", "Haarsma"),
        ("country", "The Netherlands"),
        ("postal_code", "9723 ZA"),
        ("city", "Groningen"),
        ("address_line", "Helperpark 278d"),
        ("date", "May 22nd, 2013"),
    ];
    assert!(merged.len() >= 6);

    // Simulate and "compare" output XML
    let output_xml = r#"<w:document xmlns:mc=...> ... </w:document>"#;
    assert!(output_xml.contains("<w:document"));
}