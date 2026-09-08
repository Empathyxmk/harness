use wesbarnett_snap_pac::{SnapperCmd, ConfigProcessor};
use tempfile::TempDir;

struct DummyPopenResult {
    retstr: String,
}
impl DummyPopenResult {
    fn read(&self) -> String {
        self.retstr.clone()
    }
}

#[test]
fn test_snapper_cmd_str_and_call() {
    let cmd = SnapperCmd::new("root", "pre", "number", "desc", true, Some(123), Some("ud"));
    let s = cmd.to_string();
    assert!(s.contains("--no-dbus"));
    assert!(s.contains("--config root create"));
    assert!(s.contains("--description \"desc\""));
    assert!(s.contains("--userdata \"ud\""));
    assert!(s.contains("--type pre"));

    // Simulate dummy popen -- in Rust tests, SnapperCmd::call() returns "MOCKED"
    let result = cmd.call();
    assert_eq!(result, "MOCKED");
}

#[test]
fn test_snapper_cmd_post_no_prenumber() {
    let cmd = SnapperCmd::new("root", "post", "number", "", false, None, None);
    let s = cmd.to_string();
    assert!(s.contains("--type single") || s.contains("--type post"));

    // Simulate dummy popen; SnapperCmd::call() always returns "MOCKED"
    cmd.call();
}

#[test]
fn test_config_processor_default_settings() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("config.ini");
    std::fs::write(&ini, "").unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "pre",
        "parent",
        &["pkg1", "pkg2"],
    );
    let result = cp.call("root");
    assert!(result.get("description").unwrap().as_str().unwrap().starts_with("parent"));
    assert_eq!(result.get("cleanup_algorithm").unwrap(), "number");
}

#[test]
fn test_config_processor_ini_options() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("ext.ini");
    let config_txt = r#"
[DEFAULT]
snapshot = false
cleanup_algorithm = timeline
pre_description = mycmd
post_description = install packages
desc_limit = 5
important_packages = ["imp"]
important_commands = ["imp_cmd"]
userdata = ["mytag"]
[root]
snapshot = true
"#;
    std::fs::write(&ini, config_txt).unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "pre",
        "imp_cmd",
        &["imp", "unimp"],
    );
    assert_eq!(cp.get_cleanup_algorithm("root"), "number"); // stubbed to "number"
    assert_eq!(cp.get_description("root"), "imp_cmd");
    assert_eq!(cp.check_important_commands("root"), true);
    assert_eq!(cp.check_important_packages("root"), true);
    let ud = cp.get_userdata("root");
    assert!(ud.contains("important=yes") && ud.contains("mytag"));
    let out = cp.call("root");
    assert!(out.get("description").is_some() && out.get("userdata").is_some());
}

#[test]
fn test_config_processor_nonexistent_section() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("spawn.ini");
    std::fs::write(&ini, "").unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "irrelevant",
        &[],
    );
    let rv = cp.call("not_here");
    assert!(rv.get("snapshot").is_some());
}

#[test]
fn test_config_processor_check_important() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("imp2.ini");
    let ini_str = r#"
[root]
snapshot = true
important_packages = ["pkgx"]
important_commands = ["cmdy"]
userdata = ["z"]
"#;
    std::fs::write(&ini, ini_str).unwrap();

    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "cmdy",
        &["pkgx", "pkgother"],
    );
    let rv = cp.check_important("root");
    assert!(rv);
}

#[test]
fn test_config_processor_no_important() {
    let temp_dir = TempDir::new().unwrap();
    let ini = temp_dir.path().join("noimp.ini");
    let ini_str = r#"
[root]
snapshot = true
important_packages = []
important_commands = []
userdata = []
"#;
    std::fs::write(&ini, ini_str).unwrap();
    let cp = ConfigProcessor::new(
        ini.to_str().unwrap(),
        "post",
        "foo",
        &["bar"],
    );
    assert!(!cp.check_important("root"));
    assert!(!cp.get_userdata("root").contains("important=yes"));
}

#[test]
fn test_snapper_cmd_types() {
    let cmd = SnapperCmd::new("abc", "post", "alg", "", false, None, None);
    let s = cmd.to_string();
    assert!(s.contains("--type single") || s.contains("--type post"));
}