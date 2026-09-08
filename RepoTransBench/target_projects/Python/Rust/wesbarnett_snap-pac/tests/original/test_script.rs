use std::path::Path;
use std::collections::HashMap;
use std::env;
use wesbarnett_snap_pac::{
    check_skip, get_snapper_configs, SnapperCmd, ConfigProcessor, Prefile
};

#[test]
fn test_snapper_cmd() {
    let cases = vec![
        (
            SnapperCmd::new("root", "pre", "number", "foo", false, None, None),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"foo\" --type pre"
        ),
        (
            SnapperCmd::new("root", "post", "number", "bar", false, Some(1234), None),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
        ),
        (
            SnapperCmd::new("root", "post", "number", "bar", true, Some(1234), None),
            "snapper --no-dbus --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
        ),
        (
            SnapperCmd::new("root", "post", "number", "bar", false, Some(1234), Some("important=yes")),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"important=yes\" --pre-number 1234 --type post"
        ),
        (
            SnapperCmd::new("root", "post", "number", "bar", false, Some(1234), Some("foo=bar,important=yes")),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --pre-number 1234 --type post"
        ),
        (
            SnapperCmd::new("root", "post", "number", "bar", false, None, Some("foo=bar,important=yes")),
            "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --type single"
        ),
    ];

    for (snapper_cmd, actual_cmd) in cases {
        assert_eq!(snapper_cmd.to_string(), actual_cmd);
    }
}

#[test]
fn test_get_snapper_configs() {
    let mut f = tempfile::NamedTempFile::new().unwrap();
    writeln!(f, "## Path: System/Snapper").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "## Type:        string").unwrap();
    writeln!(f, "## Default:     \"\"").unwrap();
    writeln!(f, "# List of snapper configurations.").unwrap();
    writeln!(f, "SNAPPER_CONFIGS=\"home root foo bar\"").unwrap();
    let path = f.path();
    let result = get_snapper_configs(path);
    assert_eq!(result, vec![
        "home".to_string(),
        "root".to_string(),
        "foo".to_string(),
        "bar".to_string()
    ]);
}

#[test]
fn test_skip_snap_pac() {
    env::set_var("SNAP_PAC_SKIP", "y");
    assert!(check_skip());
}

#[test]
fn test_config_processor() {
    let mut f = tempfile::NamedTempFile::new().unwrap();
    writeln!(f, "[root]").unwrap();
    writeln!(f, "important_commands = [\"pacman -Syu\"]").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "[home]").unwrap();
    writeln!(f, "snapshot = True").unwrap();
    writeln!(f, "desc_limit = 3").unwrap();
    writeln!(f, "post_description = a really long description").unwrap();
    writeln!(f, "userdata = [\"foo=bar\", \"requestid=42\"]").unwrap();
    writeln!(f, "").unwrap();
    writeln!(f, "[myconfig]").unwrap();
    writeln!(f, "snapshot = True").unwrap();
    writeln!(f, "cleanup_algorithm = timeline").unwrap();
    writeln!(f, "important_packages = [\"linux\", \"linux-lts\"]").unwrap();
    writeln!(f, "userdata = [\"foo=bar\", \"requestid=42\"]").unwrap();

    let config_path = f.path().to_string_lossy().into_owned();
    let processor = ConfigProcessor::new(
        &config_path,
        "pre",
        "pacman -Syu",
        &[],
    );
    let out = processor.call("root");
    assert_eq!(out.get("description").unwrap(), "pacman -Syu");
    assert_eq!(out.get("cleanup_algorithm").unwrap(), "number");
    assert!(out.get("userdata").is_some());
    assert!(out.get("snapshot").is_some());
}

#[test]
fn test_prefile_read_none() {
    let prefile = Prefile::new("root", "pre");
    assert_eq!(prefile.read(), None);
}

#[test]
fn test_prefile_read() {
    let prefile = Prefile::new("root", "pre");
    prefile.write("1234");
    let prefile2 = Prefile::new("root", "post");
    prefile2.write("1234"); // simulate prior write
    assert_eq!(prefile2.read(), Some("1234".into()));
}

#[test]
fn test_no_prefile() {
    let prefile = Prefile::new("foo-pre-file-not-found", "post");
    assert_eq!(prefile.read(), None);
}