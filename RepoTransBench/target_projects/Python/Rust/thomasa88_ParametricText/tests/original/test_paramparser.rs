use parametric_text::paramparser::{ParamSpec, nullint};
use parametric_text::paramparser::SliceSpec;

#[test]
fn test_from_string_basic() {
    let ps = ParamSpec::from_string("foo").unwrap();
    assert_eq!(ps, ParamSpec::new("foo", None, None, None));
}

#[test]
fn test_from_string_with_member() {
    let ps = ParamSpec::from_string("foo.bar").unwrap();
    assert_eq!(ps, ParamSpec::new("foo", Some("bar"), None, None));
}

#[test]
fn test_from_string_with_slice() {
    let ps = ParamSpec::from_string("foo[2]").unwrap();
    assert_eq!(ps, ParamSpec::new("foo", None, Some(SliceSpec{start: Some(2), end: Some(3)}), None));

    let ps2 = ParamSpec::from_string("foo[1:3]").unwrap();
    assert_eq!(ps2, ParamSpec::new("foo", None, Some(SliceSpec{start: Some(1), end: Some(3)}), None));

    let ps3 = ParamSpec::from_string("foo[:4]").unwrap();
    assert_eq!(ps3, ParamSpec::new("foo", None, Some(SliceSpec{start: None, end: Some(4)}), None));

    let ps4 = ParamSpec::from_string("foo[-2:]").unwrap();
    assert_eq!(ps4, ParamSpec::new("foo", None, Some(SliceSpec{start: Some(-2), end: None}), None));
}

#[test]
fn test_from_string_with_format() {
    let ps = ParamSpec::from_string("foo:0.2f").unwrap();
    assert_eq!(ps, ParamSpec::new("foo", None, None, Some("0.2f")));
    let ps2 = ParamSpec::from_string("foo.bar[0:2]:spec").unwrap();
    assert_eq!(ps2, ParamSpec::new("foo", Some("bar"), Some(SliceSpec{start: Some(0), end: Some(2)}), Some("spec")));
}

#[test]
fn test_from_string_invalid() {
    assert!(ParamSpec::from_string("bad[").is_none());
}

#[test]
fn test_eq() {
    let a = ParamSpec::new("foo", Some("bar"), Some(SliceSpec{start:Some(1),end:Some(2)}), Some("fmt"));
    let b = ParamSpec::new("foo", Some("bar"), Some(SliceSpec{start:Some(1),end:Some(2)}), Some("fmt"));
    let c = ParamSpec::new("foo", Some("baz"), Some(SliceSpec{start:Some(1),end:Some(2)}), Some("fmt"));
    assert_eq!(a, b);
    assert_ne!(a, c);
}

#[test]
fn test_nullint() {
    assert_eq!(nullint("3"), Some(3));
    assert_eq!(nullint(""), None);
}