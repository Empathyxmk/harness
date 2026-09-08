use std::collections::HashMap;

struct DummyConn;

struct DummyRedis {
    pub url: Option<String>,
    pub kwargs: Option<HashMap<String, String>>,
}

impl DummyRedis {
    fn from_url(url: &str, kwargs: HashMap<String, String>) -> DummyConn {
        assert!(url.starts_with("redis://"));
        assert!(!kwargs.is_empty());
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
fn test_flaskredis_init_app_different_url() {
    let mut config = HashMap::new();
    config.insert("APP2_URL".to_string(), "redis://127.0.0.1:6382/5".to_string());
    let mut app = App::new(config);
    let mut kwargs = HashMap::new();
    kwargs.insert("foo".to_string(), "barbazquux".to_string());
    let _conn = DummyRedis::from_url(&app.config["APP2_URL"], kwargs.clone());
    app.extensions.insert("app2".to_string(), 1);
    assert_eq!(app.config["APP2_URL"], "redis://127.0.0.1:6382/5");
    assert_eq!(app.extensions.get("app2"), Some(&1));
}

#[test]
fn test_from_custom_provider_diff_url() {
    struct OtherProvider;
    impl OtherProvider {
        fn from_url(url: &str, kwargs: HashMap<String, String>) -> &'static str {
            assert_eq!(url, "redis://192.168.1.2:6399/6");
            assert_eq!(kwargs.get("baropt").unwrap(), "bartest99");
            "hello-ext"
        }
    }
    let mut config = HashMap::new();
    config.insert("REDIS_URL".to_string(), "redis://192.168.1.2:6399/6".to_string());
    let mut app = App::new(config);
    let mut kwargs = HashMap::new();
    kwargs.insert("baropt".to_string(), "bartest99".to_string());
    let _ = OtherProvider::from_url(&app.config["REDIS_URL"], kwargs);
    app.extensions.insert("redis".to_string(), 1);
    assert_eq!(app.extensions.get("redis"), Some(&1));
}

#[test]
fn test_flaskredis_basic_instance() {
    #[derive(Default)]
    struct FlaskRedis { config_prefix: String }
    let r = FlaskRedis { config_prefix: "BAR".to_string() };
    assert_eq!(r.config_prefix, "BAR");
}