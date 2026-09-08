use protontricks::_version;

#[test]
fn test_public_version_attributes() {
    assert_eq!(_version::__version__.matches('.').count(), 2);
    // There's no tuple of unknown size, but (0,0,0) always.
    assert_eq!(_version::version_tuple.len(), 3);
    assert!(_version::__version__.starts_with(&format!("{}", _version::version_tuple.0)));
}