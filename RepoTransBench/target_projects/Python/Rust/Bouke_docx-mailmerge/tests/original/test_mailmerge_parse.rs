#[test]
fn test_parse_instr_valid() {
    let instr = "MERGEFIELD  somefield  \\* MERGEFORMAT";
    let name = parse_mergefield_instr(instr);
    assert_eq!(name, Some("somefield".to_string()));
}

#[test]
fn test_parse_instr_invalid() {
    let instr = "SOMETHINGELSE testing";
    let name = parse_mergefield_instr(instr);
    assert_eq!(name, None);
}

#[test]
fn test_parse_instr_quoted() {
    let instr = r#"MERGEFIELD "another field""#;
    let name = parse_mergefield_instr(instr);
    assert_eq!(name, Some("another field".to_string()));
}

/// Simulates the private __parse_instr Python function as best as possible in Rust
fn parse_mergefield_instr(instr: &str) -> Option<String> {
    if instr.starts_with("MERGEFIELD") {
        let instr_rest = &instr["MERGEFIELD".len()..];
        let mut instr_rest = instr_rest.trim();
        if instr_rest.starts_with('"') {
            // Quoted field
            let end = instr_rest[1..].find('"')?;
            Some(instr_rest[1..1+end].to_string())
        } else {
            // First word
            let mut parts = instr_rest.split_whitespace();
            parts.next().map(|s| s.to_string())
        }
    } else {
        None
    }
}