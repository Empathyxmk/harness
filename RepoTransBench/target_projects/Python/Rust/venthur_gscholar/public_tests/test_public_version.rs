use venthur_gscholar::gscholar as gs;

#[test]
fn test_public_version_string() {
    assert!(gs::__VERSION__.is_ascii());
    assert!(gs::__VERSION__.len() >= 1);
}

#[test]
fn test_public_version_not_empty() {
    assert_ne!(gs::__VERSION__, "");
}

#[test]
fn test_public_version_contains_dot() {
    assert!(gs::__VERSION__.contains("."));
}