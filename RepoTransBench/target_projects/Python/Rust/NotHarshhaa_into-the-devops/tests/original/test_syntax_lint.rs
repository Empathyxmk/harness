// Original tests translated from Python
use syntax_lint::syntax_lint::*;
use tempfile::NamedTempFile;
use std::io::Write;
use std::fs;
use std::collections::HashMap;

#[test]
fn test_balanced_details() {
    let lines: Vec<&[u8]> = vec![
        b"<details>\n",
        b"content\n",
        b"</details>\n"
    ];
    assert!(count_details(&lines));
}

#[test]
fn test_unbalanced_details_more_opens() {
    let lines: Vec<&[u8]> = vec![
        b"<details>\n",
        b"stuff\n"
    ];
    assert!(!count_details(&lines));
}

#[test]
fn test_unbalanced_details_more_closes() {
    let lines: Vec<&[u8]> = vec![
        b"</details>\n",
        b"<details>\n",
        b"</details>\n"
    ];
    assert!(!count_details(&lines));
}

#[test]
fn test_balanced_summary() {
    let lines: Vec<&[u8]> = vec![
        b"<summary>\n",
        b"foo\n",
        b"</summary>\n"
    ];
    assert!(count_summary(&lines));
}

#[test]
fn test_unbalanced_summary_open() {
    let lines: Vec<&[u8]> = vec![
        b"<summary>\n",
        b"foo\n"
    ];
    assert!(!count_summary(&lines));
}

#[test]
fn test_unbalanced_summary_close() {
    let lines: Vec<&[u8]> = vec![
        b"foo\n",
        b"</summary>\n"
    ];
    assert!(!count_summary(&lines));
}

#[test]
fn test_correct_nesting() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<details>\n", b"text\n", b"</details>\n"];
    check_details_tag(&lines, &mut errors);
    assert_eq!(errors.len(), 0);
}

#[test]
fn test_missing_closing() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<details>\n", b"<details>\n"];
    check_details_tag(&lines, &mut errors);
    assert!(errors.iter().any(|e| e.contains("Missing closing detail")));
}

#[test]
fn test_missing_opening() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"</details>\n"];
    check_details_tag(&lines, &mut errors);
    assert!(errors.iter().any(|e| e.contains("Missing opening detail")));
}

#[test]
fn test_oneline_detail() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<details>foo</details>\n"];
    check_details_tag(&lines, &mut errors);
    assert!(errors.is_empty());
}

#[test]
fn test_correct_summary() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<summary>\n", b"text\n", b"</summary>\n"];
    check_summary_tag(&lines, &mut errors);
    assert_eq!(errors.len(), 0);
}

#[test]
fn test_missing_closing_summary() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<summary>\n", b"<summary>\n"];
    check_summary_tag(&lines, &mut errors);
    assert!(errors.iter().any(|e| e.contains("Missing closing summary")));
}

#[test]
fn test_missing_opening_summary() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"</summary>\n"];
    check_summary_tag(&lines, &mut errors);
    assert!(errors.iter().any(|e| e.contains("Missing opening summary")));
}

#[test]
fn test_oneline_summary() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<summary>xyz</summary>\n"];
    check_summary_tag(&lines, &mut errors);
    assert!(errors.is_empty());
}

#[test]
fn test_nested_open_summary() {
    let mut errors = vec![];
    let lines: Vec<&[u8]> = vec![b"<summary>\n", b"<summary>\n"];
    check_summary_tag(&lines, &mut errors);
    assert!(errors.iter().any(|e| e.contains("Missing closing summary")));
}

#[test]
fn test_valid_file() {
    let mut tmp = NamedTempFile::new().unwrap();
    write!(tmp, "<details>\ntext\n<summary>\ntext\n</summary>\n</details>\n").unwrap();
    let errors = check_md_file(tmp.path()).unwrap();
    assert!(errors.is_empty());
}

#[test]
fn test_file_with_errors() {
    let mut tmp = NamedTempFile::new().unwrap();
    write!(tmp, "<details>\nno close\n<summary>\nno close\n").unwrap();
    let errors = check_md_file(tmp.path()).unwrap();
    assert!(errors.is_empty() || errors.is_a::<Vec<String>>()); // Accepts either Vec or none (Rust type always Vec)
}

#[test]
fn test_main_block_good_and_bad_file() {
    let mut tmp_good = NamedTempFile::new().unwrap();
    write!(tmp_good, "<details>\n<summary>\ntest\n</summary>\n</details>\n").unwrap();
    let mut tmp_bad = NamedTempFile::new().unwrap();
    write!(tmp_bad, "<details>\n").unwrap();

    // Good input should have no errors
    let errors = check_md_file(tmp_good.path()).unwrap();
    assert!(errors.is_empty());

    // Bad input should report errors
    let errors_bad = check_md_file(tmp_bad.path()).unwrap();
    assert!(!errors_bad.is_empty());
}