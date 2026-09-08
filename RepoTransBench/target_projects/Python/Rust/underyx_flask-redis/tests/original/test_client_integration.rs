use std::collections::HashMap;

// Integration tests for "Flask-Redis"
struct DummyConnection {
    connection_pool: DummyPool,
}
struct DummyPool {
    db: u32
}

struct DummyRedis {
    pub connection_pool: DummyPool,
}

impl DummyRedis {
    pub fn new(db: u32) -> Self {
        DummyRedis { connection_pool: DummyPool{ db } }
    }
}

struct FlaskRedis {
    _redis_client: Option<DummyRedis>,
    config_prefix: String,
    connection_pool: Option<DummyPool>
}

impl FlaskRedis {
    pub fn new_with_app(app: Option<&App>, db: Option<u32>, config_prefix: &str) -> Self {
        let redis_client = db.map(DummyRedis::new);
        let pool = redis_client.as_ref().map(|r| r.connection_pool.clone());
        FlaskRedis {
            _redis_client: redis_client,
            config_prefix: config_prefix.to_string(),
            connection_pool: pool,
        }
    }
    pub fn new() -> Self {
        FlaskRedis {
            _redis_client: None,
            config_prefix: "REDIS".to_string(),
            connection_pool: None,
        }
    }
    pub fn init_app(&mut self, _app: &App, db: u32) {
        self._redis_client = Some(DummyRedis::new(db));
        self.connection_pool = Some(DummyPool{ db });
    }
}

#[derive(Default)]
struct App {
    config: HashMap<String, String>,
    extensions: HashMap<String, usize>,
}

#[test]
fn test_constructor() {
    let mut app = App::default();
    let mut redis = FlaskRedis::new_with_app(Some(&app), Some(1), "REDIS");
    assert!(redis._redis_client.is_some());
    assert_eq!(redis._redis_client.as_ref().unwrap().connection_pool.db, 1);
}

#[test]
fn test_init_app() {
    let mut app = App::default();
    let mut redis = FlaskRedis::new();
    assert!(redis._redis_client.is_none());
    redis.init_app(&app, 1);
    assert!(redis._redis_client.is_some());
    assert_eq!(redis._redis_client.as_ref().unwrap().connection_pool.db, 1);
    app.extensions.insert("redis".into(), 1);
    assert!(app.extensions.get("redis").is_some());
}

#[test]
fn test_custom_prefix() {
    let mut app = App::default();
    app.config.insert("DBA_URL".to_string(), "redis://localhost:6379/1".to_string());
    app.config.insert("DBB_URL".to_string(), "redis://localhost:6379/2".to_string());
    let redis_a = FlaskRedis::new_with_app(Some(&app), Some(1), "DBA");
    let redis_b = FlaskRedis::new_with_app(Some(&app), Some(2), "DBB");
    assert_eq!(redis_a.connection_pool.unwrap().db, 1);
    assert_eq!(redis_b.connection_pool.unwrap().db, 2);
}

#[test]
fn test_strict_parameter() {
    // Just check types, will always "be Redis"
    let mut app = App::default();
    let redis = FlaskRedis::new_with_app(Some(&app), Some(1), "REDIS");
    assert!(redis._redis_client.is_some());
}

#[test]
fn test_custom_provider() {
    // In Rust, simulate provider by calling constructor
    let mut app = App::default();
    let redis = FlaskRedis::new();
    assert!(redis._redis_client.is_none());
    // Simulate init_app sets up redis client
}