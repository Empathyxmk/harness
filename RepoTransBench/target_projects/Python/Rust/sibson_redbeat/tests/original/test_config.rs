// Translation of tests/test_config.py

struct FakeAppConf {
    broker_url: String,
    redbeat_key_prefix: Option<String>,
    redbeat_lock_key: Option<String>,
}

struct FakeRedBeatConfig {
    app: FakeAppConf,
    lock_timeout: Option<u32>,
    key_prefix: String,
    schedule_key: String,
    statics_key: String,
    lock_key: Option<String>,
    schedule: Option<std::collections::HashMap<String, String>>,
}

impl FakeRedBeatConfig {
    fn new(app: &FakeAppConf) -> Self {
        let key_prefix = app.redbeat_key_prefix.clone().unwrap_or_else(|| "redbeat:".to_string());
        let lock_key = match &app.redbeat_lock_key {
            Some(k) if k.is_empty() => Some(key_prefix.clone()),
            Some(k) => Some(format!("{}{}", key_prefix, k)),
            None => None,
        };
        let schedule_key = format!("{}:schedule", key_prefix);
        let statics_key = format!("{}:statics", key_prefix);
        let lock_key_field = lock_key.clone();
        Self {
            app: app.clone(),
            lock_timeout: None,
            key_prefix,
            schedule_key,
            statics_key,
            lock_key: lock_key_field,
            schedule: None,
        }
    }
    fn either_or(&self, key: &str) -> String {
        format!("either_or_{}", key)
    }
}

impl Clone for FakeAppConf {
    fn clone(&self) -> Self {
        Self {
            broker_url: self.broker_url.clone(),
            redbeat_key_prefix: self.redbeat_key_prefix.clone(),
            redbeat_lock_key: self.redbeat_lock_key.clone(),
        }
    }
}

#[test]
fn test_redbeat_config_app() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("redbeat:".to_string()),
        redbeat_lock_key: None,
    };
    let conf = FakeRedBeatConfig::new(&app);
    assert_eq!(conf.key_prefix, "redbeat:");
}

#[test]
fn test_redbeat_config_lock_timeout() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("redbeat:".to_string()),
        redbeat_lock_key: None,
    };
    let conf = FakeRedBeatConfig::new(&app);
    assert_eq!(conf.lock_timeout, None);
}

#[test]
fn test_redbeat_config_other_keys() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("redbeat:".to_string()),
        redbeat_lock_key: None,
    };
    let conf = FakeRedBeatConfig::new(&app);
    assert_eq!(conf.schedule_key, "redbeat::schedule");
    assert_eq!(conf.statics_key, "redbeat::statics");
}

#[test]
fn test_redbeat_config_key_prefix_override() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("test-prefix:".to_string()),
        redbeat_lock_key: None,
    };
    let conf = FakeRedBeatConfig::new(&app);
    assert_eq!(conf.key_prefix, "test-prefix:");
}

#[test]
fn test_redbeat_config_lock_key_override() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("redbeat:".to_string()),
        redbeat_lock_key: Some(":custom".to_string()),
    };
    let conf = FakeRedBeatConfig::new(&app);
    assert_eq!(conf.lock_key.as_deref(), Some("redbeat::custom"));
}

#[test]
fn test_redbeat_config_schedule_setter() {
    let app = FakeAppConf {
        broker_url: "redis://localhost".to_string(),
        redbeat_key_prefix: Some("redbeat:".to_string()),
        redbeat_lock_key: None,
    };
    let mut conf = FakeRedBeatConfig::new(&app);
    let schedule = std::collections::HashMap::<String, String>::new();
    conf.schedule = Some(schedule.clone());
    assert_eq!(conf.schedule.as_ref(), Some(&schedule));
}