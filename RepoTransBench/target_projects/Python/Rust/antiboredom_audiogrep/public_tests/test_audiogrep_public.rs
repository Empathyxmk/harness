use antiboredom_audiogrep::*;
use tempfile::tempdir;
use std::fs;
use std::io::Write;

#[test]
fn test_get_files_public() {
    let tmp = tempdir().unwrap();
    let a = tmp.path().join("file1.aac");
    let b = tmp.path().join("file2.m4a");
    let c = tmp.path().join("file3.txt");
    for f in [&a, &b, &c] {
        let mut file = fs::File::create(f).unwrap();
        write!(file, "test abc").unwrap();
    }
    let fs = get_files(tmp.path(), &[".aac", ".m4a"]);
    let expected = vec![a.to_string_lossy().to_string(), b.to_string_lossy().to_string()];
    assert_eq!(std::collections::HashSet::<_>::from_iter(fs.iter()), std::collections::HashSet::from_iter(expected.iter()));
}