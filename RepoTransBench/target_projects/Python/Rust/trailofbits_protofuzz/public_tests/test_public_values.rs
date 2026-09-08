use crate::values;

#[test]
fn test_integral_value_gen_public() {
    let vals: Vec<_> = values::integral_value_gen().collect();
    assert!(vals.iter().all(|v| v.is_integer()));
    assert!(vals.len() > 5);
    assert_eq!(vals.len(), vals.iter().copied().collect::<std::collections::HashSet<_>>().len());
    assert!(vals.iter().any(|v| *v < 0) && vals.iter().any(|v| *v >= 0));
}

#[test]
fn test_float32_value_gen_public() {
    let vals: Vec<_> = values::float32_value_gen().collect();
    assert!(vals.iter().all(|v| v.is_finite()));
    assert!(vals.len() > 7);
    assert_eq!(vals.len(), vals.iter().copied().collect::<std::collections::HashSet<_>>().len());
    assert!(vals.iter().any(|v| v.abs() < 1.0));
    assert!(vals.iter().any(|v| v.abs() > 1.0));
}

#[test]
fn test_string_value_gen_public() {
    let vals: Vec<_> = values::string_value_gen().collect();
    assert!(vals.iter().all(|v| v.is_ascii()));
    assert!(vals.iter().any(|v| v.len() > 3));
    assert!(vals.len() > 5);
    assert_eq!(vals.len(), vals.iter().collect::<std::collections::HashSet<_>>().len());
}