use parametric_text::paramparser::{ParamSpec};

#[test]
fn test_ParamSpec_basic() {
    let p = ParamSpec::new("anotherparam", Some("anotherval"), None, None);
    assert_eq!(p.var, "anotherparam");
    assert_eq!(p.member.as_deref(), Some("anotherval"));
}

#[test]
fn test_ParamSpec_str() {
    let p = ParamSpec::new("customparam", Some("val42"), None, None);
    assert_eq!(p.to_string(), "(customparam, val42)");
}

#[test]
fn test_ParamSpec_eq() {
    let p1 = ParamSpec::new("eqtest", Some("a"), None, None);
    let p2 = ParamSpec::new("eqtest", Some("a"), None, None);
    let p3 = ParamSpec::new("eqtest", Some("b"), None, None);
    assert_eq!(p1, p2);
    assert_ne!(p1, p3);
}