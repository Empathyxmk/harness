use crate::values;

#[test]
fn test_integral_value_gen() {
    let mut g = values::integral_value_gen();
    let vals: Vec<_> = g.by_ref().take(8).collect();
    assert!(vals.iter().all(|v| v.is_integer()));
}

#[test]
fn test_float32_value_gen() {
    let mut g = values::float32_value_gen();
    let vals: Vec<_> = g.by_ref().take(8).collect::<Vec<_>>();
    assert!(vals.iter().all(|v| v.is_finite()));
}

#[test]
fn test_string_value_gen() {
    let mut g = values::string_value_gen();
    let vals: Vec<_> = g.by_ref().take(6).collect::<Vec<_>>();
    assert!(vals.iter().all(|v| v.is_ascii()));
}