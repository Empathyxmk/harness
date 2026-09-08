use aadhithya_rajiniPP::*;

#[test]
fn test_version_and_str() {
    // Test __version__ and __version_str__ existence and contents
    assert_eq!(__version__, "1.2.3");
    assert!(__version_str__.contains("rajini++"));
    // Test __all__ presence
    assert!(!__all__.is_empty());
}

#[test]
fn test_rpp_runner_imported() {
    // rpp should be an instance of runner::RppRunner
    let rpp = runner::RppRunner::new();
    // (In Python: isinstance(rajinipp.rpp, RppRunner))
    let _: &runner::RppRunner = &rpp;
}