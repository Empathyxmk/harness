use seatgeek_fuzzywuzzy::fuzz;

#[test]
fn test_ratio_symmetric() {
    let cases = vec![
        ("abc", "abc"),
        ("abc", "cab"),
        ("", ""),
        ("fast car", "car fast"),
        ("test", ""),
        ("", "test"),
    ];
    for (a, b) in cases {
        assert_eq!(fuzz::ratio(a, b), fuzz::ratio(b, a), "Symmetry property for ratio failed on ('{}', '{}')", a, b);
    }
}

#[test]
fn test_partial_ratio_symmetric() {
    let cases = vec![
        ("abc", "abc"),
        ("abc", "cab"),
        ("", ""),
        ("fast car", "car fast"),
        ("test", ""),
        ("", "test"),
    ];
    for (a, b) in cases {
        assert_eq!(fuzz::partial_ratio(a, b), fuzz::partial_ratio(b, a),
            "Symmetry property for partial_ratio failed on ('{}', '{}')", a, b);
    }
}

#[test]
fn test_ratio_identity() {
    let samples = vec!["a", "abc", "", "with space", "123"];
    for s in samples {
        assert_eq!(fuzz::ratio(s, s), 100, "Identity property for ratio failed on '{}'", s);
    }
}