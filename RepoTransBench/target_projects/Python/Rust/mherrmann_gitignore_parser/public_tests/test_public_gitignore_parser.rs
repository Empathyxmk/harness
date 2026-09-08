use std::fs;
use std::path::Path;
use std::os::unix::fs::symlink;

use tempfile::tempdir;

use mherrmann_gitignore_parser::{parse_gitignore, parse_gitignore_str};

#[test]
fn test_simple() {
    let matches = parse_gitignore_str(
        "build/\n*.log",
        "/example"
    );
    assert!(!matches("/example/main.txt"));
    assert!(matches("/example/main.log"));
    assert!(matches("/example/dir/main.log"));
    assert!(matches("/example/build"));
}

#[test]
fn test_simple_parse_file() {
    let temp_dir = tempdir().unwrap();
    let gitignore_path = temp_dir.path().join(".gitignore");
    fs::write(
        &gitignore_path,
        "dist/\n*.tmp"
    ).unwrap();
    let matches = parse_gitignore(&gitignore_path);
    let base = temp_dir.path().to_string_lossy();
    assert!(!matches(format!("{}/app.py", base)));
    assert!(matches(format!("{}/app.tmp", base)));
    assert!(matches(format!("{}/sub/app.tmp", base)));
    assert!(matches(format!("{}/dist", base)));
}

#[test]
fn test_incomplete_filename() {
    let matches = parse_gitignore_str("app.js", "/public");
    assert!(matches("/public/app.js"));
    assert!(!matches("/public/test.js"));
    assert!(!matches("/public/app.jsx"));
    assert!(matches("/public/dir/app.js"));
    assert!(!matches("/public/dir/test.js"));
    assert!(!matches("/public/dir/app.jsx"));
}

#[test]
fn test_wildcard() {
    let matches = parse_gitignore_str(
        "error.*",
        "/tmp"
    );
    assert!(matches("/tmp/error.txt"));
    assert!(matches("/tmp/error.bak/"));
    assert!(matches("/tmp/dir/error.txt"));
    assert!(matches("/tmp/error."));
    assert!(!matches("/tmp/error"));
    assert!(!matches("/tmp/errorX"));
}

#[test]
fn test_anchored_wildcard() {
    let matches = parse_gitignore_str(
        "/success.*",
        "/dirfoo"
    );
    assert!(matches("/dirfoo/success.txt"));
    assert!(matches("/dirfoo/success.c"));
    assert!(!matches("/dirfoo/a/success.java"));
}

#[test]
fn test_trailingspaces() {
    let matches = parse_gitignore_str(
        "ignoretailspace \n\
        notignoredspace\\ \n\
        almostignoredspace\\  \n\
        almostignoredspace2 \\  \n\
        notignoredmultiplespace\\ \\ \\ ",
        "/abc"
    );
    assert!(matches("/abc/ignoretailspace"));
    assert!(!matches("/abc/ignoretailspace "));
    assert!(matches("/abc/almostignoredspace "));
    assert!(!matches("/abc/almostignoredspace  "));
    assert!(!matches("/abc/almostignoredspace"));
    assert!(matches("/abc/almostignoredspace2  "));
    assert!(!matches("/abc/almostignoredspace2   "));
    assert!(!matches("/abc/almostignoredspace2 "));
    assert!(!matches("/abc/almostignoredspace2"));
    assert!(matches("/abc/notignoredspace "));
    assert!(!matches("/abc/notignoredspace"));
    assert!(matches("/abc/notignoredmultiplespace   "));
    assert!(!matches("/abc/notignoredmultiplespace"));
}

#[test]
fn test_comment() {
    let matches = parse_gitignore_str(
        "firstmatch\n\
        #notrealcomment\n\
        secondmatch\n\
        \\#reallyamatch",
        "/bdir"
    );
    assert!(matches("/bdir/firstmatch"));
    assert!(!matches("/bdir/#notrealcomment"));
    assert!(matches("/bdir/secondmatch"));
    assert!(matches("/bdir/#reallyamatch"));
}

#[test]
fn test_ignore_directory() {
    let matches = parse_gitignore_str("cache/", "/mnt");
    assert!(matches("/mnt/cache"));
    assert!(matches("/mnt/cache/subdir"));
    assert!(matches("/mnt/cache/file.txt"));
    assert!(!matches("/mnt/cachex"));
    assert!(!matches("/mnt/cache_v2.py"));
}

#[test]
fn test_ignore_directory_asterisk() {
    let matches = parse_gitignore_str("output/*", "/results");
    assert!(!matches("/results/output"));
    assert!(matches("/results/output/folder"));
    assert!(matches("/results/output/file.txt"));
}

#[test]
fn test_negation() {
    let matches = parse_gitignore_str(
        "*.bak\n!keep.bak",
        "/store"
    );
    assert!(matches("/store/junk.bak"));
    assert!(!matches("/store/keep.bak"));
    assert!(matches("/store/lost.bak"));
}

#[test]
fn test_literal_exclamation_mark() {
    let matches = parse_gitignore_str(
        "\\!saveit!", "/fs"
    );
    assert!(matches("/fs/!saveit!"));
    assert!(!matches("/fs/saveit!"));
    assert!(!matches("/fs/saveit"));
}

#[test]
fn test_double_asterisks() {
    let matches = parse_gitignore_str(
        "dir/**/Final", "/abc"
    );
    assert!(matches("/abc/dir/sub/Final"));
    assert!(matches("/abc/dir/foo/Final"));
    assert!(matches("/abc/dir/Final"));
    assert!(!matches("/abc/dir/Finals"));
}

#[test]
fn test_double_asterisk_without_slashes_handled_like_single_asterisk() {
    let matches = parse_gitignore_str("m/n**o/p", "/usr");
    assert!(matches("/usr/m/no/p"));
    assert!(matches("/usr/m/nko/p"));
    assert!(matches("/usr/m/nno/p"));
    assert!(matches("/usr/m/noo/p"));
    assert!(!matches("/usr/m/nop"));
    assert!(!matches("/usr/m/n/o/p"));
    assert!(!matches("/usr/m/nn/oo/p"));
    assert!(!matches("/usr/m/nn/YY/oo/p"));
}

#[test]
fn test_more_asterisks_handled_like_single_asterisk() {
    let matches = parse_gitignore_str("***z/x", "/sample");
    assert!(matches("/sample/ABCz/x"));
    assert!(!matches("/sample/yyy/z/x"));
    let matches2 = parse_gitignore_str("z/x***", "/sample");
    assert!(matches2("/sample/z/xABC"));
    assert!(!matches2("/sample/z/x/abc"));
}

#[test]
fn test_directory_only_negation() {
    let matches = parse_gitignore_str(
        "content/**\n!content/**/\n!.hold\n!content/01_data/*",
        "/vault"
    );
    assert!(!matches("/vault/content/01_data/"));
    assert!(!matches("/vault/content/01_data/.hold"));
    assert!(!matches("/vault/content/01_data/doc.csv"));
    assert!(!matches("/vault/content/02_final/"));
    assert!(!matches("/vault/content/02_final/.hold"));
    assert!(matches("/vault/content/02_final/summary.txt"));
}

#[test]
fn test_single_asterisk() {
    let matches = parse_gitignore_str("*", "/misc");
    assert!(matches("/misc/note.txt"));
    assert!(matches("/misc/folder"));
    assert!(matches("/misc/folder-trailing/"));
}

#[test]
fn test_supports_path_type_argument() {
    let matches = parse_gitignore_str("image1\n!image2", "/photos");
    assert!(matches(&Path::new("/photos/image1")));
    assert!(!matches(&Path::new("/photos/image2")));
}

#[test]
fn test_slash_in_range_does_not_match_dirs() {
    let matches = parse_gitignore_str("pqr[S-U/]stu", "/zdir");
    assert!(!matches("/zdir/pqrststu"));
    assert!(matches("/zdir/pqrSstu"));
    assert!(matches("/zdir/pqrTstu"));
    assert!(matches("/zdir/pqrUstu"));
    assert!(!matches("/zdir/pqr/stu"));
    assert!(!matches("/zdir/pqrSTUstu"));
}

#[test]
fn test_symlink_to_another_directory() {
    let root_dir = tempdir().unwrap();
    let other_dir = tempdir().unwrap();
    let matches = parse_gitignore_str("linker", root_dir.path().to_str().unwrap());
    let link_path = root_dir.path().join("linker");
    symlink(&other_dir.path(), &link_path).unwrap();
    assert!(matches(&link_path));
    assert!(!matches(&root_dir.path().join("link")));
}