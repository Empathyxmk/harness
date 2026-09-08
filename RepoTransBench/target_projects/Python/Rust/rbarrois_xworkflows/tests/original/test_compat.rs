use rbarrois_xworkflows::compat;

#[test]
fn test_import_compat_direct_src() {
    assert_eq!(compat::u("abc"), "abc");
    let s: &str = "test";
    let i: i32 = 123;
    assert!(compat::is_string(&s));
    assert!(!compat::is_string(&i));
    assert!(!compat::is_string(&(None::<i32>)));
}

#[test]
fn test_import_compat_from_src_direct() {
    // Direct use of compat API
    assert_eq!(compat::u("def"), "def");
    let abc = "abc";
    assert!(compat::is_string(&abc));
    let v: Vec<i32> = vec![];
    assert!(!compat::is_string(&v));
}

#[test]
fn test_python2_mode_equivalence() {
    let hey = String::from("hey");
    let bytes = b"bytes";
    assert!(compat::is_string(&hey));
    assert!(!compat::is_string(&bytes));
}