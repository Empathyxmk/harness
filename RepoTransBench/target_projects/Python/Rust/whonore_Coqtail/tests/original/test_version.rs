use coqtail::version::*;

#[test]
fn test_parse_version_cases() {
    let cases = vec![
        ("1.2.3", (1, 2, 3)),
        ("1.2pl3", (1, 2, 3)),
        ("1.2", (1, 2, 0)),
        ("1.2+alpha3", (1, 2, 0)),
        ("1.2+alpha", (1, 2, 0)),
    ];
    for (s, expected) in cases {
        assert_eq!(parse_version(s), expected);
    }
}

#[test]
fn test_compare_version() {
    assert!(compare_version((8, 17, 0), (8, 16, 5)) > 0);
    assert!(compare_version((8, 7, 1), (8, 8, 0)) < 0);
}