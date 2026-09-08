use peritus_bumpversion::version_part::VersionPart;

#[test]
fn test_public_version_part_value_setting() {
    let vp = VersionPart::new("7");
    assert_eq!(vp.value, "7");
}

#[test]
fn test_public_version_part_compare_different_values() {
    let vp1 = VersionPart::new("3");
    let vp2 = VersionPart::new("10");
    assert_ne!(vp1, vp2);
}

#[test]
fn test_public_version_part_equality_with_same_value() {
    let vp1 = VersionPart::new("hello");
    let vp2 = VersionPart::new("hello");
    assert_eq!(vp1, vp2);
}

#[test]
fn test_public_version_part_repr() {
    let vp = VersionPart::new("2024");
    assert!(format!("{:?}", vp).contains("2024"));
}

#[test]
fn test_public_version_part_str_cast() {
    let vp = VersionPart::new("543");
    assert_eq!(format!("{}", vp), "543");
}

#[test]
fn test_public_version_part_int_cast() {
    let vp = VersionPart::new("8");
    let iv: i32 = (&vp).into();
    assert_eq!(iv, 8);
}

#[test]
#[should_panic]
fn test_public_version_part_int_cast_non_numeric() {
    let vp = VersionPart::new("xyz");
    let _iv: i32 = (&vp).into(); // Should panic
}