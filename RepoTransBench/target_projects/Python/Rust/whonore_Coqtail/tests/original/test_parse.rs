use coqtail::parse::*;

#[test]
fn test_is_ident() {
    assert!(is_ident("KappaZetaXYZ"));
    assert!(is_ident("T2X9P"));
    assert!(!is_ident("10MainVar"));
    assert!(!is_ident("_bad"));
    assert!(!is_ident(""));
}

#[test]
fn test_split_line() {
    let text = "Theorem Power: forall n, n ^ 2 >= 0.";
    let result = split_line(text);
    assert_eq!(result.0, "Theorem Power");
    assert!(result.1.contains("forall"));
}

#[test]
fn test_find_name() {
    let text = "Theorem my_power: forall n, n ^ 2 >= 0.";
    let name = find_name(text);
    assert_eq!(name.unwrap(), "my_power");
}