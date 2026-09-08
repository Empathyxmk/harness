use protontricks::_version;

#[test]
fn test_version_attributes() {
    assert_eq!(_version::__version__, "0.0.0");
    assert_eq!(_version::version, "0.0.0");
    assert_eq!(_version::version_tuple, (0, 0, 0));
}