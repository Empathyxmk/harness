use crate::config::Config;
use std::path::PathBuf;
use std::env;
use std::fs::File;
use std::io::Write;

#[test]
fn test_config_custom_path() {
    let tmp = env::temp_dir();
    let tmpfile = tmp.join("different_test_pyproject.toml");
    let mut f = File::create(&tmpfile).unwrap();
    let _ = f.write_all(b"[tool.pytest-watcher]\n");
    let conf = Config::with_path(tmpfile.clone());
    assert_eq!(conf.path, tmpfile);
    // cleanup
    let _ = std::fs::remove_file(tmpfile);
}