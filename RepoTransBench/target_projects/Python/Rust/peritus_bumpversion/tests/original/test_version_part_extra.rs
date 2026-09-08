use peritus_bumpversion::version_part::*;

#[test]
fn test_version_part_default() {
    let vp = VersionPart::new("1");
    assert_eq!(vp.value, "1");
    assert!(!vp.is_optional());
    assert_eq!(vp.copy(), vp);
    assert!(format!("{}", vp).is_ascii());
    assert!(format!("{:?}", vp).contains("VersionPart"));
    let vp_bumped = vp.bump();
    assert_eq!(vp_bumped.value, "2");
}

#[test]
fn test_version_part_with_configured() {
    let cfg = ConfiguredVersionPartConfiguration::new(vec!["a", "b"]);
    let vp = VersionPart::new("a");
    let vp2 = VersionPart::new(cfg.bump("a"));
    assert_eq!(vp.value, "a");
    assert_eq!(vp2.value, "b");
}

#[test]
fn test_version_part_null_and_eq() {
    let cfg = NumericVersionPartConfiguration::new();
    let vp = VersionPart::new("4");
    let null_vp = vp.null();
    assert_eq!(null_vp.value, cfg.first_value);
    assert_ne!(vp, null_vp);
    let vp2 = VersionPart::new("4");
    assert_eq!(vp, vp2);
}

#[test]
fn test_part_config_properties() {
    let cfg = NumericVersionPartConfiguration::new();
    assert_eq!(cfg.first_value, "0");
    assert_eq!(cfg.optional_value, "0");
    assert_eq!(cfg.bump("9"), "10");
}