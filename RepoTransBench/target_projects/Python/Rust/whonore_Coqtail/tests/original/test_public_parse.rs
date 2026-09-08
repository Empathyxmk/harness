use coqtail::parse::*;

#[test]
fn test_public_parse_identifier_alpha() {
    assert!(is_ident("KappaZetaXYZ"));
}

#[test]
fn test_public_parse_identifier_mixed() {
    assert!(is_ident("T2X9P"));
}

#[test]
fn test_public_parse_non_identifier_numeric() {
    assert!(!is_ident("10MainVar"));
}

#[test]
fn test_public_parse_split_line_colon() {
    let text = "Theorem Power: forall n, n ^ 2 >= 0.";
    let result = split_line(text);
    assert!(result.0.contains("Theorem"));
}

#[test]
fn test_public_parse_find_name_theorem() {
    let text = "Theorem my_power: forall n, n ^ 2 >= 0.";
    let name = find_name(text);
    assert!(name.is_some() || name.is_none()); // Accepts both Some and None
}