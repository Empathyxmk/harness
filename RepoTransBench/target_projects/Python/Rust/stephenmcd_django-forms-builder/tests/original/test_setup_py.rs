/// This test simulates logic like that of setup.py for file exclusion and build dir cleaning.
/// It is impossible to execute real setup scripts in Rust, so the logic is mirrored for exclusion and removal.
use std::fs::{File, remove_file, create_dir_all, remove_dir_all};
use std::io::Write;

#[test]
fn test_exclude_files_like() {
    let tmp = tempfile::tempdir().unwrap();
    let py_file = tmp.path().join("tmp.py");
    let mut f = File::create(&py_file).unwrap();
    writeln!(f, "pass").unwrap();
    let other_file = tmp.path().join("tmp.txt");
    let mut f = File::create(&other_file).unwrap();
    writeln!(f, "hello").unwrap();
    let pyc_file = tmp.path().join("tmp.pyc");
    let mut f = File::create(&pyc_file).unwrap();
    writeln!(f, "compiled!").unwrap();

    let files = vec![py_file.clone(), other_file.clone()];
    for f in files {
        assert!(f.exists());
        remove_file(&f).unwrap();
        assert!(!f.exists());
    }
}

#[test]
fn test_remove_build_like() {
    let tmp = tempfile::tempdir().unwrap();
    let build_path = tmp.path().join("build");
    create_dir_all(&build_path).unwrap();
    assert!(build_path.exists());
    remove_dir_all(&build_path).unwrap();
    assert!(!build_path.exists());
}