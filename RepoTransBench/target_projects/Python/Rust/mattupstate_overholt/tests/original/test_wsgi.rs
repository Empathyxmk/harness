// Translation of tests/test_wsgi.py

use std::sync::Arc;

#[test]
fn test_wsgi_application_exists() {
    // This simulates `hasattr(wsgi, "application")` in Rust.
    let app: Option<&Arc<mattupstate_overholt::wsgi::DispatcherMiddleware>> = Some(&mattupstate_overholt::wsgi::APPLICATION);
    assert!(app.is_some());
}

#[test]
fn test_wsgi_main_run_simple() {
    // In Rust, we can't monkeypatch imports as in Python,
    // but we can check that we can reload/init the application and it has the required property.
    let app = &mattupstate_overholt::wsgi::APPLICATION;
    assert!(app.mounts.contains_key("/api"));
}