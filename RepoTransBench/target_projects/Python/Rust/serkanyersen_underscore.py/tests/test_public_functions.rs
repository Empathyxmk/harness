// This is a PUBLIC test file.
use serkanyersen_underscore::underscore::once;

#[test]
fn test_once_public() {
    let mut called = Vec::new();

    let mut func = || {
        called.push("called");
        "foo"
    };
    let mut once_func = once(|| func());
    assert_eq!(once_func(), "foo");
    once_func();
    assert_eq!(called, vec!["called"]);
}