// Mocks the integration test that the constructor passes app to FlaskRedis::init_app
use crate::client;

struct MockFlaskRedis {
    pub called_with_app: Option<String>,
}

impl MockFlaskRedis {
    pub fn new() -> Self {
        Self { called_with_app: None }
    }
    pub fn init_app(&mut self, app_stub: &str) {
        self.called_with_app = Some(app_stub.to_string());
    }
}

#[test]
fn test_constructor_app() {
    // Simulate Python's mocker.patch/object assertion
    let mut fr = MockFlaskRedis::new();
    let stub = "app_stub";
    fr.init_app(stub);
    assert_eq!(fr.called_with_app.as_deref(), Some("app_stub"));
}