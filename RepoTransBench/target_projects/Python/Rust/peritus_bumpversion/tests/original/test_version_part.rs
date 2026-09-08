use peritus_bumpversion::version_part::*;

#[test]
fn test_version_part_init() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    assert_eq!(vp.value, confvpc.first_value);
}

#[test]
fn test_version_part_copy() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    let vc = vp.copy();
    assert_eq!(vp.value, vc.value);
}

#[test]
fn test_version_part_bump() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    let vc = vp.bump();
    assert_eq!(vc.value, (confvpc.first_value.parse::<u64>().unwrap()+1).to_string());
}

#[test]
fn test_version_part_check_optional_false() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    let b = vp.bump();
    assert!(!b.is_optional());
}

#[test]
fn test_version_part_check_optional_true() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    assert!(vp.is_optional());
}

#[test]
fn test_version_part_format() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    assert_eq!(format!("{}", vp), confvpc.first_value);
}

#[test]
fn test_version_part_equality() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    let vp2 = VersionPart::new(confvpc.first_value.clone());
    assert_eq!(vp, vp2);
}

#[test]
fn test_version_part_null() {
    let confvpc = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new(confvpc.first_value.clone());
    let null_vp = vp.null();
    assert_eq!(null_vp.value, "0");
}