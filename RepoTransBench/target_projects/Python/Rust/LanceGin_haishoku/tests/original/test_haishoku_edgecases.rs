use haishoku_rs::haishoku::Haishoku;

#[test]
fn test_hs_instance_return_type() {
    let class_ptr = Haishoku::load_haishoku("demo/demo_01.png");
    let class_ptr2 = Haishoku::load_haishoku("demo/demo_01.png");
    assert_eq!(class_ptr as *const _, class_ptr2 as *const _);
}