use haishoku_rs::haishoku::Haishoku;

#[test]
fn test_hs_instance() {
    // The test expects load_haishoku to return the class itself.
    let class_ptr = Haishoku::load_haishoku("demo/demo_01.png");
    // We can test that it is actually the static instance, which acts as a "class"
    // or at least, the test must confirm that calling the function gives a constant address.
    let class_ptr2 = Haishoku::load_haishoku("demo/demo_01.png");
    assert_eq!(class_ptr as *const _, class_ptr2 as *const _);
}