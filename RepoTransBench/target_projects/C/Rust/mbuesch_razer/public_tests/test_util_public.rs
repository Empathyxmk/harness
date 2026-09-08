fn test_dummy_public() -> i32 {
    99
}

#[test]
fn test_util_public() {
    assert_eq!(test_dummy_public(), 99);
    println!("test_util_public passed");
}