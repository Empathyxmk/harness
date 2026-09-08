use crate::runner::helper::*;

#[test]
fn test_that_get_class_name_works_with_a_string_instance() {
    let s = String::from("abc");
    assert_eq!("str", cls_name(s));
}

#[test]
fn test_that_get_class_name_works_with_a_4() {
    let n = 4i32;
    assert_eq!("int", cls_name(n));
}

#[test]
fn test_that_get_class_name_works_with_a_tuple() {
    let t = (3, "pie", vec![]);
    assert_eq!("tuple", cls_name(t));
}