use aadhithya_rajiniPP::*;

#[test]
fn test_public_version_and_str() {
    // Existence and type
    assert_eq!(__version__, "1.2.3");
    assert!(__version_str__.starts_with("rajini"));
    // __all__ is non-empty
    assert!(!__all__.is_empty());
}

#[test]
fn test_public_rpp_runner_imported() {
    let rpp = runner::RppRunner::new();
    let typename = std::any::type_name::<runner::RppRunner>();
    assert!(typename.contains("RppRunner"));
}