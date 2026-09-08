use peritus_bumpversion::functions::*;

#[test]
fn test_numeric_function_basic_bump() {
    let nf = NumericFunction::new(Some("3")).unwrap();
    assert_eq!(nf.bump("3"), "4");
    assert_eq!(nf.bump("99"), "100");
}

#[test]
fn test_numeric_function_first_value_and_optional_value() {
    let nf = NumericFunction::new(Some("00")).unwrap();
    assert_eq!(nf.first_value, "00");
    assert_eq!(nf.optional_value, "00");
}

#[test]
fn test_numeric_function_alphanumeric() {
    let nf = NumericFunction::new(Some("r3")).unwrap();
    assert_eq!(nf.bump("r3"), "r4");
    let nf2 = NumericFunction::new(Some("r3-001")).unwrap();
    assert_eq!(nf2.bump("r3-001"), "r4-001");
}

#[test]
fn test_numeric_function_invalid_first_value() {
    let nf = NumericFunction::new(Some("abc"));
    assert!(nf.is_err());
}

#[test]
#[should_panic] // Will panic on no digit found
fn test_numeric_function_no_digits() {
    let n = NumericFunction::new(None).unwrap();
    let _ = n.bump("abc");
}

#[test]
fn test_values_function_bump_and_errors() {
    let vf = ValuesFunction::new(vec!["alpha", "beta", "rc", "final"].iter().map(|s| s.to_string()).collect(), None, None).unwrap();
    assert_eq!(vf.bump(&"alpha".to_string()).unwrap(), "beta".to_string());
    assert_eq!(vf.bump(&"beta".to_string()).unwrap(), "rc".to_string());
    assert_eq!(vf.bump(&"rc".to_string()).unwrap(), "final".to_string());
    assert!(vf.bump(&"final".to_string()).is_err());
}

#[test]
fn test_values_function_invalid_empty() {
    let vf = ValuesFunction::<String>::new(vec![], None, None);
    assert!(vf.is_err());
}

#[test]
fn test_values_function_optional_value_not_in_values() {
    let vf = ValuesFunction::new(vec!["a".to_string(), "b".to_string()], Some("c".to_string()), None);
    assert!(vf.is_err());
}

#[test]
fn test_values_function_first_value_not_in_values() {
    let vf = ValuesFunction::new(vec!["a".to_string(), "b".to_string()], None, Some("c".to_string()));
    assert!(vf.is_err());
}