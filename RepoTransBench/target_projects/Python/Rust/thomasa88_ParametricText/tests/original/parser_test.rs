use parametric_text::paramparser::{ParamSpec, SliceSpec};

#[test]
fn test_split_param() {
    assert_eq!(ParamSpec::from_string("_"), Some(ParamSpec::new("_", None, None, None)));
    assert_eq!(ParamSpec::from_string("_.version"), Some(ParamSpec::new("_", Some("version"), None, None)));
    assert_eq!(ParamSpec::from_string("_.version:02d"), Some(ParamSpec::new("_", Some("version"), None, Some("02d"))));
    assert_eq!(
        ParamSpec::from_string("_.file[1:5]"),
        Some(ParamSpec::new("_", Some("file"), Some(SliceSpec{start:Some(1), end:Some(5)}), None))
    );
    assert_eq!(
        ParamSpec::from_string("_.file[1:5]:01"),
        Some(ParamSpec::new("_", Some("file"), Some(SliceSpec{start:Some(1), end:Some(5)}), Some("01")))
    );
    assert_eq!(ParamSpec::from_string("param"), Some(ParamSpec::new("param", None, None, None)));
    assert_eq!(ParamSpec::from_string("param:-<2"), Some(ParamSpec::new("param", None, None, Some("-<2"))));
    assert_eq!(ParamSpec::from_string("param[1]:-<2"), Some(ParamSpec::new("param", None, Some(SliceSpec{start:Some(1), end:Some(2)}), Some("-<2"))));
    assert_eq!(ParamSpec::from_string("param[-1:]"), Some(ParamSpec::new("param", None, Some(SliceSpec{start:Some(-1), end:None}), None)));
    assert_eq!(ParamSpec::from_string("param[:-3]"), Some(ParamSpec::new("param", None, Some(SliceSpec{start:None, end:Some(-3)}), None)));
}

#[test]
fn test_slice_parsing() {
    assert_eq!(ParamSpec::from_string("p[0]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(0), end:Some(1)}), None)));
    assert_eq!(ParamSpec::from_string("p[:5]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:None, end:Some(5)}), None)));
    assert_eq!(ParamSpec::from_string("p[6:]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(6), end:None}), None)));
    assert_eq!(ParamSpec::from_string("p[5:6]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(5), end:Some(6)}), None)));
    assert_eq!(ParamSpec::from_string("p[:-1]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:None, end:Some(-1)}), None)));
    assert_eq!(ParamSpec::from_string("p[1:-2]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(1), end:Some(-2)}), None)));

    assert_eq!(ParamSpec::from_string("p[:]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:None, end:None}), None)));
    assert_eq!(ParamSpec::from_string("p[-5:5]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(-5), end:Some(5)}), None)));
    assert_eq!(ParamSpec::from_string("p[11:5]"), Some(ParamSpec::new("p", None, Some(SliceSpec{start:Some(11), end:Some(5)}), None)));

    assert_eq!(ParamSpec::from_string("p[]"), None);
    assert_eq!(ParamSpec::from_string("p[a]"), None);
    assert_eq!(ParamSpec::from_string("p[a:b]"), None);
    assert_eq!(ParamSpec::from_string("p[:b]"), None);
    assert_eq!(ParamSpec::from_string("p[1:3:2]"), None);
    assert_eq!(ParamSpec::from_string("p[::]"), None);
}

#[test]
fn test_split_example_strings() {
    assert_eq!(ParamSpec::from_string("d1:.3f"), Some(ParamSpec::new("d1", None, None, Some(".3f"))));
    assert_eq!(ParamSpec::from_string("d1.unit"), Some(ParamSpec::new("d1", Some("unit"), None, None)));
    assert_eq!(ParamSpec::from_string("d1:03.0f"), Some(ParamSpec::new("d1", None, None, Some("03.0f"))));
    assert_eq!(ParamSpec::from_string("width:.0f"), Some(ParamSpec::new("width", None, None, Some(".0f"))));
    assert_eq!(ParamSpec::from_string("width.expr"), Some(ParamSpec::new("width", Some("expr"), None, None)));
    assert_eq!(ParamSpec::from_string("height.expr"), Some(ParamSpec::new("height", Some("expr"), None, None)));
    assert_eq!(ParamSpec::from_string("_.version"), Some(ParamSpec::new("_", Some("version"), None, None)));
    assert_eq!(ParamSpec::from_string("_.version:03"), Some(ParamSpec::new("_", Some("version"), None, Some("03"))));
    assert_eq!(ParamSpec::from_string("_.file"), Some(ParamSpec::new("_", Some("file"), None, None)));
    assert_eq!(ParamSpec::from_string("_.component"), Some(ParamSpec::new("_", Some("component"), None, None)));
    assert_eq!(ParamSpec::from_string("_.date"), Some(ParamSpec::new("_", Some("date"), None, None)));
    assert_eq!(ParamSpec::from_string("_.date:%m/%d/%Y"), Some(ParamSpec::new("_", Some("date"), None, Some("%m/%d/%Y"))));
    assert_eq!(ParamSpec::from_string("_.date:%U"), Some(ParamSpec::new("_", Some("date"), None, Some("%U"))));
    assert_eq!(ParamSpec::from_string("_.date:%W"), Some(ParamSpec::new("_", Some("date"), None, Some("%W"))));
    assert_eq!(ParamSpec::from_string("_.date:%H:%M"), Some(ParamSpec::new("_", Some("date"), None, Some("%H:%M"))));
}

#[test]
fn test_bad_param_string() {
    let bad_strings = [
        "",
        ".",
        ".a",
        "a.",
        ".a[10]",
        ".a:5",
        ".[]",
        "a[]",
        "[]",
        ":",
        "a[",
        "a]",
        "[1]",
        "a[1",
        ":5",
        "a[10:10][]",
    ];
    for bad in bad_strings.iter() {
        assert_eq!(ParamSpec::from_string(bad), None, "Input: {:?}", bad);
    }
}