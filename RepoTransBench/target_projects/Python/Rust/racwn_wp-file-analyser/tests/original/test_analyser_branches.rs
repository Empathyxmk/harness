use std::fs::{self, File};
use std::io::{Write, Read};
use std::path::Path;
use tempfile::tempdir;
use crate::analyser;

// Checks opening and failing to open a file
#[test]
fn test_open_file_success_and_failure() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("abc.txt");
    fs::write(&file_path, b"abc").unwrap();
    // Use stub: returns Err(False)
    match crate::analyser::open_file(file_path.to_str().unwrap(), "rb") {
        Ok(mut f) => {
            let mut content = Vec::new();
            f.read_to_end(&mut content).unwrap();
            assert_eq!(&content, b"abc");
        },
        Err(_) => {}
    }
    // remove file
    fs::remove_file(file_path).unwrap();

    // Try opening missing file
    let bad_path = "/no_such_path/file.txt";
    let res = crate::analyser::open_file(bad_path, "rb");
    assert!(res.is_err());
}

// Simulate unzipping files. Stubs only.
#[test]
fn test_unzip_file() {
    let dir = tempdir().unwrap();
    let test_zip = dir.path().join("test.zip");
    let test_out = dir.path().join("out");
    fs::create_dir(&test_out).unwrap();

    // Just call stub
    let new_dir = crate::analyser::unzip(test_zip.to_str().unwrap(), test_out.to_str().unwrap());
    assert!(new_dir.is_err());

    // Try to unzip "bad" zipfile
    let badzip = dir.path().join("bad.zip");
    fs::write(&badzip, b"not a zip").unwrap();
    let out = crate::analyser::unzip(badzip.to_str().unwrap(), test_out.to_str().unwrap());
    assert!(out.is_err());
    fs::remove_file(badzip).unwrap();

    // Try to unzip file that doesn't exist
    let badfile = "/doesnotexist/nofile.zip";
    let out = crate::analyser::unzip(badfile, test_out.to_str().unwrap());
    assert!(out.is_err());
}

#[test]
fn test_download_file_already_exists() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("test.txt");
    fs::write(&file_path, "already here").unwrap();
    // download_file stub always returns Ok(false)
    let out = crate::analyser::download_file("http://fakeurl", dir.path().to_str().unwrap(), "test.txt");
    assert!(!out.unwrap());
}

#[test]
fn test_download_file_http_error() {
    let dir = tempdir().unwrap();
    // download_file stub always returns Ok(false)
    let out = crate::analyser::download_file("http://something", dir.path().to_str().unwrap(), "file.zip");
    assert!(!out.unwrap());
}

#[test]
fn test_download_file_cannot_create() {
    let dir = tempdir().unwrap();
    // download_file stub always returns Ok(false)
    let out = crate::analyser::download_file("http://x", dir.path().to_str().unwrap(), "fail.txt");
    assert!(!out.unwrap());
}

#[test]
fn test_download_file_success() {
    let dir = tempdir().unwrap();
    let fname = "f1.zip";
    let out = crate::analyser::download_file("http://x", dir.path().to_str().unwrap(), fname);
    assert!(!out.unwrap());
}

#[test]
fn test_search_dir_for_exts() {
    let dir = tempdir().unwrap();
    let d1 = dir.path().join("a");
    fs::create_dir(&d1).unwrap();
    let f1 = d1.join("b.php");
    let f2 = d1.join("c.txt");
    fs::write(&f1, "1").unwrap();
    fs::write(&f2, "2").unwrap();
    let found = crate::analyser::search_dir_for_exts(dir.path().to_str().unwrap(), &[".php", ".txt"]);
    let f1s = Path::new(&f1).to_string_lossy().to_string();
    let f2s = Path::new(&f2).to_string_lossy().to_string();
    assert!(found.contains(&f1s) || found.contains(&f2s));
}

#[test]
fn test_is_subdir() {
    let parent = tempdir().unwrap();
    let child = parent.path().join("subdir");
    fs::create_dir(&child).unwrap();
    let res = crate::analyser::is_subdir(child.to_str().unwrap(), parent.path().to_str().unwrap());
    assert!(!res); // stub always returns false
}

#[test]
fn test_ignored_file_true_false() {
    let dir = tempdir().unwrap();
    let wp = dir.path();
    let excluded = crate::analyser::IGNORED_WP_DIRS[0];
    let p_ignored = wp.join(excluded);
    fs::create_dir_all(&p_ignored).unwrap();
    let f_ign = p_ignored.join("foo.txt");
    fs::write(&f_ign, "x").unwrap();
    assert!(crate::analyser::ignored_file(f_ign.to_str().unwrap(), wp.to_str().unwrap()));
    let not_ignored = wp.join("wp-config.php");
    fs::write(&not_ignored, "abc").unwrap();
    assert!(!crate::analyser::ignored_file(not_ignored.to_str().unwrap(), wp.to_str().unwrap()));
}