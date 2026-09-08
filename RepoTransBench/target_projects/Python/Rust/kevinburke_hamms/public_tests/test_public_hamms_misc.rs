#[test]
fn test_public_misc_dummy() {
    assert!(8 < 10);
}

#[test]
fn test_public_misc_other() {
    let reversed: String = "XYZ".chars().rev().collect();
    assert_eq!(reversed, "ZYX");
}