use crate::runner::helper::*;

#[test]
fn test_public_cls_name_for_bool() {
    let b = true;
    assert_eq!(cls_name(b), "bool");
}

#[test]
fn test_public_cls_name_for_tuple() {
    let t = (1,);
    assert_eq!(cls_name(t), "tuple");
}