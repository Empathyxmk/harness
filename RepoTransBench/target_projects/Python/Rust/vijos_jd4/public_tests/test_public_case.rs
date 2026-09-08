use vijos_jd4::case::Case;

#[test]
fn test_case_repr_diff_params() {
    let c = Case::new("test_case2", "input-42", "output-99", 15);
    let r = format!("{:?}", c);
    assert!(r.contains("test_case2"));
    assert!(r.contains("score: 15") || r.contains("score=15"));
}

#[test]
fn test_case_properties_different() {
    let c = Case::new("sampleB", "abc", "def", 8);
    assert_eq!(c.name, "sampleB");
    assert_eq!(c.input, "abc");
    assert_eq!(c.output, "def");
    assert_eq!(c.score, 8);
}

#[test]
fn test_case_eq_false() {
    let c = Case::new("eqtest2", "in", "out", 1);
    assert_ne!(c, 42);
}

#[test]
fn test_case_ordering_different_name() {
    let c1 = Case::new("case0002", "", "", 0);
    let c2 = Case::new("case0010", "", "", 0);
    assert!(c1 < c2);
}

#[test]
fn test_case_str_content() {
    let c = Case::new("visible2", "inputY", "outputY", 4);
    let s = format!("{}", c);
    assert!(s.contains("visible2") && s.contains("inputY") && s.contains("outputY") && s.contains("score=4"));
}