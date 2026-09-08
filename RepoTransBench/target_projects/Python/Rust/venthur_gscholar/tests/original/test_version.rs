use venthur_gscholar::gscholar as gs;

#[test]
fn test_version() {
    assert!(gs::__VERSION__.is_ascii());
}