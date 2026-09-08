use std::collections::HashMap;

struct DummyConn;

struct DummyRedis;

impl DummyRedis {
    fn from_url(url: &str, kwargs: HashMap<String, String>) -> DummyConn {
        assert!(url.starts_with("redis://"));
        assert!(kwargs.contains_key("password") || kwargs.contains_key("fooopt"));
        DummyConn
    }
}

struct App {
    config: HashMap<String, String>,
    extensions: HashMap<String, usize>,
}

impl App {
    fn new(config: HashMap<String, String>) -> Self {
        App { config, extensions: HashMap::new() }
    }
}

#[test]
fn test_init_app_custom_url_public() {
    let mut config = HashMap::new();
    config.insert("FOO_URL".to_string(), "redis://localhost:6380/2".to_string());
    let mut app = App::new(config);
    let mut kwargs = HashMap::new();
    kwargs.insert("password".to_string(), "letmein".to_string());
    let _conn = DummyRedis::from_url(&app.config["FOO_URL"], kwargs.clone());
    app.extensions.insert("foo".to_string(), 1);
    assert_eq!(app.config["FOO_URL"], "redis://localhost:6380/2");
    assert_eq!(app.extensions.get("foo"), Some(&1));
}

#[test]
fn test_from_custom_provider_public() {
    struct CustomProvider;
    impl CustomProvider {
        fn from_url(url: &str, kwargs: HashMap<String, String>) -> &'static str {
            assert_eq!(url, "redis://localhost:6381/4");
            assert_eq!(*kwargs.get("fooopt").unwrap(), "99".to_string());
            "custom-conn"
        }
    }
    let mut config = HashMap::new();
    config.insert("REDIS_URL".to_string(), "redis://localhost:6381/4".to_string());
    let mut app = App::new(config);
    let mut kwargs = HashMap::new();
    kwargs.insert("fooopt".to_string(), "99".to_string());
    let _ = CustomProvider::from_url(&app.config["REDIS_URL"], kwargs);
    app.extensions.insert("redis".to_string(), 1);
    assert_eq!(app.extensions.get("redis"), Some(&1));
}