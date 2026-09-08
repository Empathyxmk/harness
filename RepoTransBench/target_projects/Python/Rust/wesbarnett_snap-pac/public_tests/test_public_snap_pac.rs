use wesbarnett_snap_pac::SnapperCmd;
use wesbarnett_snap_pac::ConfigProcessor;
use tempfile::TempDir;

#[test]
fn test_public_snapper_cmd_str_and_call() {
    let cmd = SnapperCmd::new("data", "pre", "timeline", "my-desc", true, Some(789), Some("user_data"));
    let s = cmd.to_string();
    assert!(s.contains("--no-dbus"));
    assert!(s.contains("--config data create"));
    assert!(s.contains("--description \"my-desc\""));
    assert!(s.contains("--userdata \"user_data\""));
    assert!(s.contains("--type pre"));

    let result = cmd.call();
    assert_eq!(result, "MOCKED");
}

#[test]
fn test_public_snapper_cmd_post_no_prenumber() {
    let cmd = SnapperCmd::new("foo", "post", "timeline", "", false, None, None);
    let s = cmd.to_string();
    assert!(s.contains("--type single") || s.contains("--type post"));
    cmd.call();
}

#[test]
fn test_public_config_processor_default_settings() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("another_config.ini");
    std::fs::write(&ini, "").unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "runjob",
        &["abc", "xyz"],
    );
    let result = cp.call("home");
    assert!(result.get("description").unwrap().as_str().unwrap().starts_with("abc")
        || result.get("description").unwrap().as_str().unwrap().starts_with("runjob")
        || result.get("description").unwrap().as_str().unwrap().starts_with("xyz"));
    assert_eq!(result.get("cleanup_algorithm").unwrap(), "number");
}

#[test]
fn test_public_config_processor_ini_options() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("more.ini");
    let config_txt = r#"
[DEFAULT]
snapshot = true
cleanup_algorithm = number
pre_description = commandX
post_description = just_test
desc_limit = 6
important_packages = ["abc"]
important_commands = ["ccc"]
userdata = ["newtag"]
[home]
snapshot = false
"#;
    std::fs::write(&ini, config_txt).unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "pre",
        "ccc",
        &["abc", "wxy"],
    );
    assert_eq!(cp.get_cleanup_algorithm("home"), "number");
    assert_eq!(cp.get_description("home"), "ccc");
    assert_eq!(cp.check_important_commands("home"), true);
    assert_eq!(cp.check_important_packages("home"), true);
    let ud = cp.get_userdata("home");
    assert!(ud.contains("important=yes") && ud.contains("newtag"));
    let out = cp.call("home");
    assert!(out.get("description").is_some() && out.get("userdata").is_some());
}

#[test]
fn test_public_config_processor_nonexistent_section() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("section.ini");
    std::fs::write(&ini, "").unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "pre",
        "diff",
        &[],
    );
    let rv = cp.call("qwerty");
    assert!(rv.get("snapshot").is_some());
}

#[test]
fn test_public_config_processor_check_important() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("zzz.ini");
    let ini_str = r#"
[home]
snapshot = false
important_packages = ["specialpkg"]
important_commands = ["specialcmd"]
userdata = ["t"]
"#;
    std::fs::write(&ini, ini_str).unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "specialcmd",
        &["specialpkg", "otherpkg"],
    );
    let rv = cp.check_important("home");
    assert!(rv);
}

#[test]
fn test_public_config_processor_no_important() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("notag.ini");
    let ini_str = r#"
[zzz]
snapshot = false
important_packages = []
important_commands = []
userdata = []
"#;
    std::fs::write(&ini, ini_str).unwrap();
    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "nope",
        &["nil"],
    );
    assert!(!cp.check_important("zzz"));
    assert!(!cp.get_userdata("zzz").contains("important=yes"));
}

#[test]
fn test_public_snapper_cmd_types() {
    let cmd = SnapperCmd::new("customcfg", "post", "otheralg", "", false, None, None);
    let s = cmd.to_string();
    assert!(s.contains("--type single") || s.contains("--type post"));
}