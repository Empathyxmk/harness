// Translation of public_tests/test_public_wsgi.py

use mattupstate_overholt::wsgi::APPLICATION;
use std::sync::Arc;

#[test]
fn test_public_wsgi_application_type() {
    // APPLICATION is Arc<DispatcherMiddleware>
    assert!(Arc::strong_count(&APPLICATION) >= 1);
}

#[test]
fn test_public_wsgi_application_mapping() {
    let app = &APPLICATION;
    assert!(app.mounts.contains_key("/api"));
}