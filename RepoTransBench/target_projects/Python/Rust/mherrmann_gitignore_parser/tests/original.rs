use std::fs;
use std::path::Path;
use std::os::unix::fs::symlink;

use tempfile::tempdir;

use mherrmann_gitignore_parser::{parse_gitignore, parse_gitignore_str, rule_from_pattern, IgnoreRule};

#[test]
fn test_some_error_branches() {
    // From extra_tests.py
    let rule = rule_from_pattern("/////");
    assert_eq!(rule.pattern, "/////");
}

#[test]
fn test_simple() {
    let matches = parse_gitignore_str(
        "__pycache__/\n*.py[cod]",
        "/home/michael"
    );
    assert!(!matches(&"/home/michael/main.py"));
    assert!(matches(&"/home/michael/main.pyc"));
    assert!(matches(&"/home/michael/dir/main.pyc"));
    assert!(matches(&"/home/michael/__pycache__"));
}

#[test]
fn test_simple_parse_file() {
    let temp_dir = tempdir().unwrap();
    let gitignore_path = temp_dir.path().join(".gitignore");
    fs::write(
        &gitignore_path,
        "__pycache__/\n*.py[cod]"
    ).unwrap();
    let matches = parse_gitignore(&gitignore_path);
    let base = temp_dir.path().to_string_lossy();
    assert!(!matches(&format!("{}/main.py", base)));
    assert!(matches(&format!("{}/main.pyc", base)));
    assert!(matches(&format!("{}/dir/main.pyc", base)));
    assert!(matches(&format!("{}/__pycache__", base)));
}

#[test]
fn test_incomplete_filename() {
    let matches = parse_gitignore_str("o.py", "/home/michael");
    assert!(matches(&"/home/michael/o.py"));
    assert!(!matches(&"/home/michael/foo.py"));
    assert!(!matches(&"/home/michael/o.pyc"));
    assert!(matches(&"/home/michael/dir/o.py"));
    assert!(!matches(&"/home/michael/dir/foo.py"));
    assert!(!matches(&"/home/michael/dir/o.pyc"));
}

#[test]
fn test_wildcard() {
    let matches = parse_gitignore_str(
        "hello.*",
        "/home/michael"
    );
    assert!(matches(&"/home/michael/hello.txt"));
    assert!(matches(&"/home/michael/hello.foobar/"));
    assert!(matches(&"/home/michael/dir/hello.txt"));
    assert!(matches(&"/home/michael/hello."));
    assert!(!matches(&"/home/michael/hello"));
    assert!(!matches(&"/home/michael/helloX"));
}

#[test]
fn test_anchored_wildcard() {
    let matches = parse_gitignore_str(
        "/hello.*",
        "/home/michael"
    );
    assert!(matches(&"/home/michael/hello.txt"));
    assert!(matches(&"/home/michael/hello.c"));
    assert!(!matches(&"/home/michael/a/hello.java"));
}

#[test]
fn test_trailingspaces() {
    let matches = parse_gitignore_str(
        "ignoretrailingspace \n\
        notignoredspace\\ \n\
        partiallyignoredspace\\  \n\
        partiallyignoredspace2 \\  \n\
        notignoredmultiplespace\\ \\ \\ ",
        "/home/michael"
    );
    assert!(matches(&"/home/michael/ignoretrailingspace"));
    assert!(!matches(&"/home/michael/ignoretrailingspace "));
    assert!(matches(&"/home/michael/partiallyignoredspace "));
    assert!(!matches(&"/home/michael/partiallyignoredspace  "));
    assert!(!matches(&"/home/michael/partiallyignoredspace"));
    assert!(matches(&"/home/michael/partiallyignoredspace2  "));
    assert!(!matches(&"/home/michael/partiallyignoredspace2   "));
    assert!(!matches(&"/home/michael/partiallyignoredspace2 "));
    assert!(!matches(&"/home/michael/partiallyignoredspace2"));
    assert!(matches(&"/home/michael/notignoredspace "));
    assert!(!matches(&"/home/michael/notignoredspace"));
    assert!(matches(&"/home/michael/notignoredmultiplespace   "));
    assert!(!matches(&"/home/michael/notignoredmultiplespace"));
}

#[test]
fn test_comment() {
    let matches = parse_gitignore_str(
        "somematch\n\
        #realcomment\n\
        othermatch\n\
        \\#imnocomment",
        "/home/michael"
    );
    assert!(matches(&"/home/michael/somematch"));
    assert!(!matches(&"/home/michael/#realcomment"));
    assert!(matches(&"/home/michael/othermatch"));
    assert!(matches(&"/home/michael/#imnocomment"));
}

#[test]
fn test_ignore_directory() {
    let matches = parse_gitignore_str(".venv/", "/home/michael");
    assert!(matches(&"/home/michael/.venv"));
    assert!(matches(&"/home/michael/.venv/folder"));
    assert!(matches(&"/home/michael/.venv/file.txt"));
    assert!(!matches(&"/home/michael/.venv_other_folder"));
    assert!(!matches(&"/home/michael/.venv_no_folder.py"));
}

#[test]
fn test_ignore_directory_asterisk() {
    let matches = parse_gitignore_str(".venv/*", "/home/michael");
    assert!(!matches(&"/home/michael/.venv"));
    assert!(matches(&"/home/michael/.venv/folder"));
    assert!(matches(&"/home/michael/.venv/file.txt"));
}

#[test]
fn test_negation() {
    let matches = parse_gitignore_str(
        "*.ignore\n!keep.ignore",
        "/home/michael"
    );
    assert!(matches(&"/home/michael/trash.ignore"));
    assert!(!matches(&"/home/michael/keep.ignore"));
    assert!(matches(&"/home/michael/waste.ignore"));
}

#[test]
fn test_literal_exclamation_mark() {
    let matches = parse_gitignore_str(
        "\\!ignore_me!", "/home/michael"
    );
    assert!(matches(&"/home/michael/!ignore_me!"));
    assert!(!matches(&"/home/michael/ignore_me!"));
    assert!(!matches(&"/home/michael/ignore_me"));
}

#[test]
fn test_double_asterisks() {
    let matches = parse_gitignore_str(
        "foo/**/Bar", "/home/michael"
    );
    assert!(matches(&"/home/michael/foo/hello/Bar"));
    assert!(matches(&"/home/michael/foo/world/Bar"));
    assert!(matches(&"/home/michael/foo/Bar"));
    assert!(!matches(&"/home/michael/foo/BarBar"));
}

#[test]
fn test_double_asterisk_without_slashes_handled_like_single_asterisk() {
    let matches = parse_gitignore_str("a/b**c/d", "/home/michael");
    assert!(matches(&"/home/michael/a/bc/d"));
    assert!(matches(&"/home/michael/a/bXc/d"));
    assert!(matches(&"/home/michael/a/bbc/d"));
    assert!(matches(&"/home/michael/a/bcc/d"));
    assert!(!matches(&"/home/michael/a/bcd"));
    assert!(!matches(&"/home/michael/a/b/c/d"));
    assert!(!matches(&"/home/michael/a/bb/cc/d"));
    assert!(!matches(&"/home/michael/a/bb/XX/cc/d"));
}

#[test]
fn test_more_asterisks_handled_like_single_asterisk() {
    let matches = parse_gitignore_str("***a/b", "/home/michael");
    assert!(matches(&"/home/michael/XYZa/b"));
    assert!(!matches(&"/home/michael/foo/a/b"));
    let matches2 = parse_gitignore_str("a/b***", "/home/michael");
    assert!(matches2(&"/home/michael/a/bXYZ"));
    assert!(!matches2(&"/home/michael/a/b/foo"));
}

#[test]
fn test_directory_only_negation() {
    let matches = parse_gitignore_str(
        "data/**\n!data/**/\n!.gitkeep\n!data/01_raw/*",
        "/home/michael"
    );
    assert!(!matches(&"/home/michael/data/01_raw/"));
    assert!(!matches(&"/home/michael/data/01_raw/.gitkeep"));
    assert!(!matches(&"/home/michael/data/01_raw/raw_file.csv"));
    assert!(!matches(&"/home/michael/data/02_processed/"));
    assert!(!matches(&"/home/michael/data/02_processed/.gitkeep"));
    assert!(matches(&"/home/michael/data/02_processed/processed_file.csv"));
}

#[test]
fn test_single_asterisk() {
    let matches = parse_gitignore_str("*", "/home/michael");
    assert!(matches(&"/home/michael/file.txt"));
    assert!(matches(&"/home/michael/directory"));
    assert!(matches(&"/home/michael/directory-trailing/"));
}

#[test]
fn test_supports_path_type_argument() {
    let matches = parse_gitignore_str("file1\n!file2", "/home/michael");
    assert!(matches(&Path::new("/home/michael/file1")));
    assert!(!matches(&Path::new("/home/michael/file2")));
}

#[test]
fn test_slash_in_range_does_not_match_dirs() {
    let matches = parse_gitignore_str("abc[X-Z/]def", "/home/michael");
    assert!(!matches(&"/home/michael/abcdef"));
    assert!(matches(&"/home/michael/abcXdef"));
    assert!(matches(&"/home/michael/abcYdef"));
    assert!(matches(&"/home/michael/abcZdef"));
    assert!(!matches(&"/home/michael/abc/def"));
    assert!(!matches(&"/home/michael/abcXYZdef"));
}

#[test]
fn test_symlink_to_another_directory() {
    let project_dir = tempdir().unwrap();
    let another_dir = tempdir().unwrap();
    let matches = parse_gitignore_str("link", project_dir.path().to_str().unwrap());
    let link = project_dir.path().join("link");
    let target = another_dir.path().join("target");
    // Create the symlink to another directory
    symlink(&target, &link).unwrap();
    // Symbolic links are not followed: only file path matters
    assert!(matches(&link));
}

#[test]
fn test_symlink_to_symlink_directory() {
    let project_dir = tempdir().unwrap();
    let link_dir = tempdir().unwrap();
    let link = link_dir.path().join("link");
    symlink(project_dir.path(), &link).unwrap();
    let file = link.join("file.txt");
    let matches = parse_gitignore_str("file.txt", link_dir.path().to_str().unwrap());
    assert!(matches(&file));
}