use parametric_text::paramformatter::{mixed_frac_inch, DummyParam, DummyDesign};

fn make_param(val: f64, unit: &str) -> DummyParam {
    DummyParam::new(val, unit)
}

#[test]
fn test_unitless_positive() {
    let p = make_param(1.75, "");
    assert_eq!(&mixed_frac_inch(&p, None), "1 3/4\"");
}

#[test]
fn test_unitless_negative() {
    let p = make_param(-2.5, "");
    assert_eq!(&mixed_frac_inch(&p, None), "-2 1/2\"");
}

#[test]
fn test_unit_inch() {
    let p = make_param(2.5, "in");
    assert_eq!(&mixed_frac_inch(&p, None), "2 1/2\"");
}

#[test]
fn test_whole_number() {
    let p = make_param(3.0, "");
    assert_eq!(&mixed_frac_inch(&p, None), "3\"");
    let p2 = make_param(0.0, "");
    assert_eq!(&mixed_frac_inch(&p2, None), "0\"");
}

#[test]
fn test_fraction_only() {
    let p = make_param(0.25, "");
    assert_eq!(&mixed_frac_inch(&p, None), "1/4\"");
    let p2 = make_param(-0.75, "");
    assert_eq!(&mixed_frac_inch(&p2, None), "-3/4\"");
}

#[test]
fn test_zero() {
    let p = make_param(0.0, "");
    assert_eq!(&mixed_frac_inch(&p, None), "0\"");
}