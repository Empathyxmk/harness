use peritus_bumpversion::version_part::VersionPart;

#[test]
fn test_public_version_part_has_value() {
    let vp = VersionPart::new("nonempty");
    assert!(vp.has_value());
}

#[test]
fn test_public_version_part_not_has_value_empty_string() {
    let vp = VersionPart::new("");
    assert!(!vp.has_value());
}

#[test]
fn test_public_version_part_int_cast_zero() {
    let vp = VersionPart::new("0");
    let iv: i32 = (&vp).into();
    assert_eq!(iv, 0);
}

#[test]
fn test_public_version_part_ignore_value() {
    let vp = VersionPart::new("ignored");
    assert_eq!(vp.value, "ignored"); // Just check the value is kept as is
}

#[test]
fn test_public_version_part_repr_contains_class() {
    let vp = VersionPart::new("classy");
    assert!(format!("{:?}", vp).contains("VersionPart"));
}