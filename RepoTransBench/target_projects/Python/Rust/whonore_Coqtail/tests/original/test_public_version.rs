use coqtail::version::*;

#[test]
fn test_public_parse_version_minor() {
    let vstr = "Coq 8.15.0 (Feb 2022)";
    let res = parse_version(vstr);
    assert_eq!(res.0, 8);
    assert_eq!(res.1, 15);
}

#[test]
fn test_public_version_compare_greater_major() {
    assert!(compare_version((8, 17, 0), (8, 16, 5)) > 0);
}

#[test]
fn test_public_version_compare_smaller_minor() {
    assert!(compare_version((8, 7, 1), (8, 8, 0)) < 0);
}