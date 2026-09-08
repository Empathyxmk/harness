use parametric_text::paramformatter::{mixed_frac_inch, DummyParam};

fn make_param(val: f64, unit: &str) -> DummyParam {
    DummyParam::new(val, unit)
}

#[test]
fn test_mixed_frac_inch_whole_number() {
    let p = make_param(15.0, "");
    // For public test, Python impl is "15" not "15\""
    let res = mixed_frac_inch(&p, None);
    assert!(res.starts_with("15"), "Expected '15', got '{}'", res);
}

#[test]
fn test_mixed_frac_inch_simple_fraction() {
    let p = make_param(0.625, "");
    let res = mixed_frac_inch(&p, None);
    assert!(res.contains("5/8"), "Expected '5/8', got '{}'", res);
}

#[test]
fn test_mixed_frac_inch_mixed() {
    let p = make_param(3.75, "");
    let res = mixed_frac_inch(&p, None);
    assert!(res.contains("3") && res.contains("3/4"), "Expected '3 3/4', got '{}'", res);
}

#[test]
fn test_mixed_frac_inch_exact_half() {
    let p = make_param(6.5, "");
    let res = mixed_frac_inch(&p, None);
    assert!(res.contains("6") && res.contains("1/2"), "Expected '6 1/2', got '{}'", res);
}

#[test]
fn test_mixed_frac_inch_zero() {
    let p = make_param(0.0, "");
    let res = mixed_frac_inch(&p, None);
    assert!(res.starts_with("0"), "Expected string starting with '0', got '{}'", res);
}