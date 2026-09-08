use std::path::Path;
use std::env;
use wesbarnett_snap_pac::{
    check_skip, get_snapper_configs, SnapperCmd, ConfigProcessor, Prefile
};

#[test]
fn test_public_snapper_cmd() {
    let cases = vec![
        (
            SnapperCmd::new("data", "pre", "timeline", "baz", false, None, None),
            "snapper --config data create --cleanup-algorithm timeline --print-number --description \"baz\" --type pre"
        ),
        (
            SnapperCmd::new("home", "post", "timeline", "qux", false, Some(4321), None),
            "snapper --config home create --cleanup-algorithm timeline --print-number --description \"qux\" --pre-number 4321 --type post"
        ),
        (
            SnapperCmd::new("data", "post", "timeline", "quux", true, Some(5678), None),
            "snapper --no-dbus --config data create --cleanup-algorithm timeline --print-number --description \"quux\" --pre-number 5678 --type post"
        ),
        (
            SnapperCmd::new("foo", "post", "timeline", "snap", false, Some(8765), Some("bar=foo")),
            "snapper --config foo create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"bar=foo\" --pre-number 8765 --type post"
        ),
        (
            SnapperCmd::new("home", "post", "timeline", "test", false, Some(2468), Some("alpha=beta,gamma=delta")),
            "snapper --config home create --cleanup-algorithm timeline --print-number --description \"test\" --userdata \"alpha=beta,gamma=delta\" --pre-number 2468 --type post"
        ),
        (
            SnapperCmd::new("data", "post", "timeline", "snap", false, None, Some("foo=bar,baz=qux")),
            "snapper --config data create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"foo=bar,baz=qux\" --type single"
        ),
    ];

    for (snapper_cmd, actual_cmd) in cases {
        assert_eq!(snapper_cmd.to_string(), actual_cmd);
    }
}

#[test]
fn test_public_get_snapper_configs() {
    let mut f = tempfile::NamedTempFile::new().unwrap();
    writeln!(f, "## Path: System/Snapper").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "## Type:        string").unwrap();
    writeln!(f, "## Default:     \"\"").unwrap();
    writeln!(f, "# List of snapper configurations.").unwrap();
    writeln!(f, "SNAPPER_CONFIGS=\"data home alpha beta\"").unwrap();
    let path = f.path();
    let result = get_snapper_configs(path);
    assert_eq!(result, vec![
        "data".to_string(),
        "home".to_string(),
        "alpha".to_string(),
        "beta".to_string()
    ]);
}

#[test]
fn test_public_skip_snap_pac() {
    env::set_var("SNAP_PAC_SKIP", "yes");
    assert!(check_skip());
}

#[test]
fn test_public_config_processor() {
    let mut f = tempfile::NamedTempFile::new().unwrap();
    writeln!(f, "[home]").unwrap();
    writeln!(f, "important_commands = [\"apt-get update\"]").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "cleanup_algorithm = timeline").unwrap();
    writeln!(f, "[beta]").unwrap();
    writeln!(f, "snapshot = True").unwrap();
    writeln!(f, "desc_limit = 5").unwrap();
    writeln!(f, "post_description = test description for beta section").unwrap();
    writeln!(f, "userdata = [\"foo=bar\", \"requestid=99\"]").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "[special]").unwrap();
    writeln!(f, "snapshot = True").unwrap();
    writeln!(f, "cleanup_algorithm = number").unwrap();
    writeln!(f, "important_packages = [\"kernel\", \"initrd\"]").unwrap();
    writeln!(f, "userdata = [\"foo=bar\", \"requestid=99\"]").unwrap();

    let config_path = f.path().to_string_lossy().into_owned();
    let processor = ConfigProcessor::new(
        &config_path,
        "pre",
        "apt-get update",
        &[],
    );
    let out = processor.call("home");
    assert!(out.get("description").is_some());
    assert!(out.get("cleanup_algorithm").is_some());
    assert!(out.get("userdata").is_some());
    assert!(out.get("snapshot").is_some());
}

#[test]
fn test_public_prefile_read_none() {
    let prefile = Prefile::new("data", "pre");
    assert_eq!(prefile.read(), None);
}

#[test]
fn test_public_prefile_read() {
    let prefile = Prefile::new("home", "pre");
    prefile.write("5678");
    let prefile2 = Prefile::new("home", "post");
    prefile2.write("5678"); // simulate prior write
    assert_eq!(prefile2.read(), Some("5678".into()));
}

#[test]
fn test_public_no_prefile() {
    let prefile = Prefile::new("nonexistent-pre-file", "post");
    assert_eq!(prefile.read(), None);
}