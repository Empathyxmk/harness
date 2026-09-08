use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use tree::{walk, Counter};

// Helper: create a directory if it doesn't exist
fn ensure_dir(path: &str) {
    if !Path::new(path).exists() {
        fs::create_dir_all(path).unwrap();
    }
}

// Helper: create a file with some contents
fn create_file(path: &str) {
    let mut f = File::create(path).unwrap();
    f.write_all(b"PUBLIC DATA\n").unwrap();
}

// Helper: recursively remove a dir tree
fn rmrf(path: &str) {
    let path = Path::new(path);
    if path.exists() {
        if path.is_dir() {
            fs::remove_dir_all(path).unwrap_or_else(|_| {
                // If remove_dir_all fails, try to remove empty directory
                fs::remove_dir(path).unwrap_or(());
            });
        } else {
            fs::remove_file(path).unwrap_or(());
        }
    }
}

#[test]
fn test_deep_structure() {
    // Setup: data_public/deep/a/b/c/file2.txt
    ensure_dir("data_public");
    ensure_dir("data_public/deep");
    ensure_dir("data_public/deep/a");
    ensure_dir("data_public/deep/a/b");
    ensure_dir("data_public/deep/a/b/c");
    create_file("data_public/deep/a/b/c/file2.txt");
    create_file("data_public/deep/fileA.txt");

    // Walk and check
    let mut c = Counter::new();
    let res = walk("data_public/deep", "", &mut c);
    
    assert!(res.is_ok());
    // Structure:
    // deep/
    // ├ a/
    // │ └ b/
    // │   └ c/
    // │      └ file2.txt
    // └ fileA.txt
    //
    // dirs: deep, deep/a, deep/a/b, deep/a/b/c => 4
    // files: deep/fileA.txt, deep/a/b/c/file2.txt => 2
    assert_eq!(c.dirs, 4);
    assert_eq!(c.files, 2);

    // Cleanup
    rmrf("data_public");
}

#[test]
fn test_multiple_files() {
    ensure_dir("data_public2");
    ensure_dir("data_public2/sub");
    ensure_dir("data_public2/sub2");
    create_file("data_public2/a.txt");
    create_file("data_public2/sub/b.txt");
    create_file("data_public2/sub2/c.txt");
    create_file("data_public2/sub2/d.txt");

    let mut c = Counter::new();
    let res = walk("data_public2", "", &mut c);
    
    assert!(res.is_ok());
    // data_public2/
    // ├ a.txt
    // ├ sub/
    // │ └ b.txt
    // └ sub2/
    //    ├ c.txt
    //    └ d.txt
    // folders: data_public2, sub, sub2 => 3
    // files: a.txt, b.txt, c.txt, d.txt => 4
    assert_eq!(c.dirs, 3);
    assert_eq!(c.files, 4);

    rmrf("data_public2");
}

#[test]
fn test_only_files() {
    ensure_dir("filespublic");
    create_file("filespublic/one.log");
    create_file("filespublic/two.log");
    create_file("filespublic/three.log");

    let mut c = Counter::new();
    let res = walk("filespublic", "", &mut c);
    
    assert!(res.is_ok());
    // One directory: filespublic
    // Three files
    assert_eq!(c.dirs, 1);
    assert_eq!(c.files, 3);

    rmrf("filespublic");
}