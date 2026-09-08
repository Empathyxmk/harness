// Implements escapes (e.g., for CSV/TSV).
fn escape_csv_field(field: &str) -> String {
    if field.contains('"') || field.contains(',') || field.contains('\n') {
        format!("\"{}\"", field.replace('"', "\"\""))
    } else {
        field.to_string()
    }
}

#[test]
fn test_escape_csv() {
    let cases = vec![
        ("a,b", "\"a,b\""),
        ("simple", "simple"),
        ("this \"quoted\"", "\"this \"\"quoted\"\"\""),
        ("with\nnewline", "\"with\nnewline\""),
    ];

    for (inp, expected) in cases {
        let got = escape_csv_field(inp);
        assert_eq!(got, expected, "failed on input {:?}", inp);
    }
}