use std::env;

#[test]
fn test_public_log_install() {
    let logger = vijos_jd4::log::logger();
    logger.info("public coloredlogs.install", ());
    assert!(true);
}

#[test]
fn test_public_log_syslog() {
    env::set_var("JD4_USE_SYSLOG", "yes");
    let logger = vijos_jd4::log::logger();
    logger.warning("public syslog", ());
    assert!(true);
    env::remove_var("JD4_USE_SYSLOG");
}

#[test]
fn test_public_config_file_not_found() {
    let config_path = std::path::Path::new("nonexistent_config.yaml");
    assert!(!config_path.exists());
    let logger = vijos_jd4::log::logger();
    logger.error("public Could not find config.yaml", ());
    assert!(true);
}