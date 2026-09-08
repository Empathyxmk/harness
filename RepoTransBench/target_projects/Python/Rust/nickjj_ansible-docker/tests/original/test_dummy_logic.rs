use nickjj_ansible_docker::dummy_logic::*;

#[test]
fn test_group_in_user_true() {
    let h = DummyHost::new();
    assert!(h.group_in_user("docker"));
}

#[test]
fn test_group_in_user_false() {
    let h = DummyHost::new();
    assert!(!h.group_in_user("other"));
}

#[test]
fn test_environment_proxy_set_true() {
    let h = DummyHost::new();
    assert!(h.environment_proxy_set().is_some());
}

#[test]
fn test_environment_proxy_set_false() {
    let mut h = DummyHost::new();
    h.environment_file = String::new();
    assert!(h.environment_proxy_set().is_none());
}

#[test]
fn test_daemon_dns_ok_true() {
    let h = DummyHost::new();
    assert!(h.daemon_dns_ok());
}

#[test]
fn test_daemon_dns_ok_false() {
    let mut h = DummyHost::new();
    h.daemon_json_content = "{\"log-driver\":\"journald\"}".to_string();
    assert!(!h.daemon_dns_ok());
}

#[test]
fn test_cron_clean_up_job_valid_true() {
    let h = DummyHost::new();
    assert!(h.cron_clean_up_job_valid());
}

#[test]
fn test_cron_clean_up_job_valid_false() {
    let mut h = DummyHost::new();
    h.cron_file = String::new();
    assert!(!h.cron_clean_up_job_valid());
}