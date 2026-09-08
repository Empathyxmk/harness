use serkanyersen_underscore::underscore::once;

#[test]
fn test_once() {
    let mut called = Vec::new();
    let mut f = || {
        called.push(1);
        3
    };

    let mut once_func = once(|| f());
    assert_eq!(once_func(), 3);
    once_func(); // Should not append again!
    assert_eq!(called, vec![1]);
}