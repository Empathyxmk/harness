use pypa_sampleproject::noxfile::{lint, DummySession};

#[test]
fn test_lint_session_exists_and_is_def() {
    // There is a 'lint' function, signature tested by compilation.
    let mut s = DummySession::new();
    lint(&mut s);
    assert!(
        !s.installed.is_empty(),
        "Installed must not be empty; indicates existence and invocation"
    );
}

#[test]
fn test_lint_session_decorator_includes_session() {
    // In Rust, the decorator analogy is that DummySession is passed as parameter.
    let mut s = DummySession::new();
    lint(&mut s);
    // No direct analog to decorator, but the function signature enforces DummySession as required.
    assert!(
        s.installed.iter().all(|a| a.contains(&"flake8".to_string())),
        "Should install flake8"
    );
}

#[test]
fn test_lint_session_calls_run_with_specific_args() {
    // Check that 'lint' runs one of "flake8", "pytest", or "mypy"
    let mut s = DummySession::new();
    lint(&mut s);
    let accepted = ["flake8", "pytest", "mypy"];
    let found = s
        .runs
        .iter()
        .flatten()
        .any(|a| accepted.iter().any(|ac| a.contains(ac)));
    assert!(
        found,
        "Should call session.run with flake8 or pytest or mypy"
    );
}