use cloudconvert_cloudconvert_rust::config;

#[test]
fn test_public_config_set_sandbox() {
    let mut cfg = config::Config::default();
    cfg.set_sandbox(true);
    assert_eq!(cfg.sandbox, true);
}

#[test]
fn test_public_config_unset_api_key() {
    let mut cfg = config::Config::default();
    assert_eq!(cfg.api_key, None);
}