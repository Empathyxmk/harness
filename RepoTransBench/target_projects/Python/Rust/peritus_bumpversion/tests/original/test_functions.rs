use peritus_bumpversion::functions::*;

#[test]
fn test_numeric_init_wo_first_value() {
    let func = NumericFunction::new(None).unwrap();
    assert_eq!(func.first_value, "0");
}

#[test]
fn test_numeric_init_w_first_value() {
    let func = NumericFunction::new(Some("5")).unwrap();
    assert_eq!(func.first_value, "5");
}

#[test]
fn test_numeric_init_non_numeric_first_value() {
    let func = NumericFunction::new(Some("a"));
    assert!(func.is_err());
}

#[test]
fn test_numeric_bump_simple_number() {
    let func = NumericFunction::new(None).unwrap();
    assert_eq!(func.bump("0"), "1");
}

#[test]
fn test_numeric_bump_prefix_and_suffix() {
    let func = NumericFunction::new(None).unwrap();
    assert_eq!(func.bump("v0b"), "v1b");
}

#[test]
fn test_values_init() {
    let func = ValuesFunction::new(vec![0, 1, 2], None, None).unwrap();
    assert_eq!(func.optional_value, 0);
    assert_eq!(func.first_value, 0);
}

#[test]
fn test_values_init_w_correct_optional_value() {
    let func = ValuesFunction::new(vec![0, 1, 2], Some(1), None).unwrap();
    assert_eq!(func.optional_value, 1);
    assert_eq!(func.first_value, 0);
}

#[test]
fn test_values_init_w_correct_first_value() {
    let func = ValuesFunction::new(vec![0, 1, 2], None, Some(1)).unwrap();
    assert_eq!(func.optional_value, 0);
    assert_eq!(func.first_value, 1);
}

#[test]
fn test_values_init_w_correct_optional_and_first_value() {
    let func = ValuesFunction::new(vec![0, 1, 2], Some(0), Some(1)).unwrap();
    assert_eq!(func.optional_value, 0);
    assert_eq!(func.first_value, 1);
}

#[test]
fn test_values_init_w_empty_values() {
    let func = ValuesFunction::<i32>::new(vec![], None, None);
    assert!(func.is_err());
}

#[test]
fn test_values_init_w_incorrect_optional_value() {
    let func = ValuesFunction::new(vec![0, 1, 2], Some(3), None);
    assert!(func.is_err());
}

#[test]
fn test_values_init_w_incorrect_first_value() {
    let func = ValuesFunction::new(vec![0, 1, 2], None, Some(3));
    assert!(func.is_err());
}

#[test]
fn test_values_bump() {
    let func = ValuesFunction::new(vec![0, 5, 10], None, None).unwrap();
    assert_eq!(func.bump(&0).unwrap(), 5);
}

#[test]
fn test_values_bump_error_on_last() {
    let func = ValuesFunction::new(vec![0, 5, 10], None, None).unwrap();
    assert!(func.bump(&10).is_err());
}