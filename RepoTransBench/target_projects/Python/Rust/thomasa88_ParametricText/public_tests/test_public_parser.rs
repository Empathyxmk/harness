use parametric_text::paramparser::{ParamSpec};

#[test]
fn test_ParamSpec_name_value() {
    let spec = ParamSpec::new("public_name", Some("17"), None, None);
    assert_eq!(spec.var, "public_name");
    assert_eq!(spec.member.as_deref(), Some("17"));
}

#[test]
fn test_ParamSpec_str_and_eq() {
    let spec1 = ParamSpec::new("ab", Some("9"), None, None);
    let spec2 = ParamSpec::new("ab", Some("9"), None, None);
    let spec3 = ParamSpec::new("ab", Some("8"), None, None);
    assert_eq!(spec1.to_string(), "(ab, 9)");
    assert_eq!(spec1, spec2);
    assert_ne!(spec1, spec3);
}