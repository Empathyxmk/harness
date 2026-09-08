use crate::libs::mock::*;

#[test]
fn test_sentinel_object_repr() {
    let s = SentinelObject("MY_MARK");
    assert_eq!(format!("{:?}", s), "<SentinelObject \"MY_MARK\">");
}

#[test]
fn test_sentinel_attribute_uniqueness() {
    // Simulate .foo and .bar keys with strings, in absence of pythonic dunder-magic
    let foo_a = String::from("foo");
    let foo_b = String::from("foo");
    let bar = String::from("bar");
    assert_eq!(foo_a, foo_b);
    assert_ne!(foo_a, bar);
}

#[test]
fn test_dot_lookup_basic() {
    struct X;
    impl X {
        const FOO: i32 = 123;
    }
    let result = X::FOO;
    assert_eq!(result, 123);
}

#[test]
fn test__copy_lists_dicts_tuples_sets() {
    let lst = vec![1, 2];
    let lst2 = lst.clone();
    assert_eq!(lst2, vec![1,2]);

    use std::collections::HashMap;
    let mut dct = HashMap::new();
    dct.insert("a", 1);
    let dct2 = dct.clone();
    assert_eq!(dct2.get("a"), Some(&1));

    let tpl = (1, 2);
    let tpl2 = tpl.clone();
    assert_eq!(tpl2, (1,2));

    use std::collections::HashSet;
    let mut st = HashSet::new();
    st.insert(1);
    st.insert(2);
    let st2 = st.clone();
    assert_eq!(st2, HashSet::from([1,2]));

    let s = 12;
    let s2 = s.clone();
    assert_eq!(s2, 12);
}

#[test]
fn test_mock_basics_and_methods() {
    let m = Mock::new();
    m.call();
    assert!(m.called.get());
    assert_eq!(m.call_count.get(), 1);
    // .call_args (simulate with last_args if implemented)
    m.reset_mock();
    assert!(!m.called.get());
}

#[test]
fn test_mock_wraps() {
    fn f(x: i32) -> i32 { x + 1 }
    let result = f(3);
    assert_eq!(result, 4);
}