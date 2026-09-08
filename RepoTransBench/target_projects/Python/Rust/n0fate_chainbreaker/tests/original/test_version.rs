use n0fate_chainbreaker::version::__version__;

#[test]
fn test_version_str() {
    assert!(__version__.contains('.'));
}