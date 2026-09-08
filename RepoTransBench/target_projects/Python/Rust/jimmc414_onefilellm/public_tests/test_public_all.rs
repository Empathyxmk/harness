// Rust translation of public_tests/test_public_all.py

use std::fs::{self, File};
use std::io::Write;
use tempfile::tempdir;
use onefilellm::utils::*;

#[test]
fn test_safe_file_read_public() {
    let tmpd = tempdir().unwrap();
    let f_utf8 = tmpd.path().join("abc.txt");
    let s = "Public 测试";
    fs::write(&f_utf8, s).unwrap();
    let content = safe_file_read(f_utf8.to_str().unwrap());
    assert_eq!(content, s);

    let f_latin1 = tmpd.path().join("latinpublic.txt");
    let text = "mañana";
    {
        let mut f = File::create(&f_latin1).unwrap();
        f.write_all(text.as_bytes()).unwrap();
    }
    assert_eq!(safe_file_read(f_latin1.to_str().unwrap()), text);
}

#[test]
fn test_file_extension_detection_public() {
    assert_eq!(get_file_extension("some.JS"), ".js");
    assert_eq!(get_file_extension("archive.TAR.GZ"), ".gz");
    assert_eq!(get_file_extension("README"), "");
    assert_eq!(get_file_extension("dots.with.many.parts.doc"), ".doc");
}

#[test]
fn test_is_binary_file_public() {
    let tmpd = tempdir().unwrap();
    let t_file = tmpd.path().join("t.txt");
    fs::write(&t_file, "Sample text").unwrap();
    assert!(!is_binary_file(t_file.to_str().unwrap()));
    let b_file = tmpd.path().join("b.dat");
    {
        let mut f = File::create(&b_file).unwrap();
        f.write_all(&[0xff, 0xd8, 0xff, 0xdb]).unwrap();
    }
    assert!(is_binary_file(b_file.to_str().unwrap()));
}

#[test]
fn test_is_excluded_file_public() {
    assert!(is_excluded_file("dist/bundle.js"));
    assert!(is_excluded_file(".git/hooks/pre-commit"));
    assert!(is_excluded_file("lib.min.js"));
    assert!(is_excluded_file("__pycache__/something.pyc"));
    assert!(is_excluded_file("node_modules/module.js"));
    assert!(!is_excluded_file("main.c"));
    assert!(!is_excluded_file("script.rb"));
}

#[test]
fn test_is_allowed_filetype_public() {
    assert!(is_allowed_filetype("index.html"));
    assert!(is_allowed_filetype("data.csv"));
    assert!(is_allowed_filetype("setup.py"));
    assert!(!is_allowed_filetype("archive.tar.gz"));
    assert!(!is_allowed_filetype("some.dll"));
    assert!(!is_allowed_filetype("compressed.rar"));
}

#[test]
fn test_url_utilities_public() {
    let base = "https://public.com/section/";
    assert!(is_same_domain(base, "https://public.com/else/"));
    assert!(!is_same_domain(base, "https://alt.com/test/"));
    assert!(is_within_depth(base, "https://public.com/section/page2", 1));
    assert!(is_within_depth(base, "https://public.com/section/inner/page", 2));
    assert!(!is_within_depth(base, "https://public.com/section/a/b/d", 2));
}

#[test]
fn test_escape_xml_public() {
    let x = "<publicTest>More & stuff</publicTest>";
    assert_eq!(escape_xml(x), x);
}