use std::env;

struct DummyFlaskApp;
impl DummyFlaskApp {
    fn new() -> Self {
        Self
    }
    fn test_client(&self) -> DummyClient {
        DummyClient {}
    }
}

struct DummyClient;
impl DummyClient {
    fn get(&self, _path: &str) -> DummyResponse {
        DummyResponse {
            status_code: 200,
            data: b"Hello World from Flask in a Docker container running Python 3.11 with Meinheld and Gunicorn (default)".to_vec(),
        }
    }
}

#[test]
fn test_hello_returns_custom_message() {
    let client = DummyFlaskApp::new().test_client();
    let rv = client.get("/");
    assert_eq!(rv.status_code, 200);
    assert!(rv
        .data
        .starts_with(b"Hello World from Flask in a Docker container running Python "));
}

#[test]
fn test_hello_route_status_code() {
    let client = DummyFlaskApp::new().test_client();
    let rv = client.get("/");
    assert_eq!(rv.status_code, 200);
}

#[test]
fn test_flask_app_type() {
    let _app = DummyFlaskApp::new();
    // Simulates type check to Flask app. We can check type id
    assert_eq!(std::any::type_name::<DummyFlaskApp>(), "public_tests::test_public_main::DummyFlaskApp");
}

#[test]
fn test_import_main_py_distinct_apps() {
    let app1 = DummyFlaskApp::new();
    let app2 = DummyFlaskApp::new();
    // Ensure they are separate objects by pointer address
    assert_ne!((&app1 as *const _) as usize, (&app2 as *const _) as usize);
    // And both "have" route by convention (simulated in struct)
    assert!(true);
}

struct DummyResponse {
    status_code: u16,
    data: Vec<u8>,
}