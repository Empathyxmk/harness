use pypa_sampleproject::noxfile::{
    build_and_check_dists, lint, tests as session_tests, DummySession,
};

#[test]
fn test_lint_runs_and_installs() {
    let mut s = DummySession::new();
    lint(&mut s);
    assert!(
        s.installed
            .iter()
            .flatten()
            .any(|arg| arg.contains("flake8")),
        "Should install flake8"
    );
    assert!(
        s.runs
            .iter()
            .flatten()
            .any(|arg| arg.contains("flake8")),
        "Should run flake8"
    );
}

#[test]
fn test_build_and_check_dists_invocations() {
    let mut s = DummySession::new();
    build_and_check_dists(&mut s);
    assert!(!s.installed.is_empty(), "Should install something");
    assert!(!s.runs.is_empty(), "Should run something");
}

#[test]
fn test_tests_invokes_build() {
    // Provide custom callback to track call
    let mut s = DummySession::new();
    let mut called = false;
    {
        let build_fn = |sess: &mut DummySession| {
            sess.runs.push(vec!["build_and_check_called".to_string()]);
            called = true;
        };
        session_tests(&mut s, Some(&build_fn));
    }
    assert!(
        called,
        "Custom build_and_check_dists function should be invoked"
    );
    assert!(
        s.runs.iter().flatten().any(|v| v == "build_and_check_called"),
        "build_and_check_called should be recorded in runs"
    );
}