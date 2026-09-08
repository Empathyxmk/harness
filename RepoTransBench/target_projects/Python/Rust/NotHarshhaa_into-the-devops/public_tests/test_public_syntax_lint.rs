// Translated from public Python tests
use syntax_lint::syntax_lint::*;
use std::collections::HashMap;

fn lines_str<'a>(slice: &[&'a str]) -> Vec<String> {
    slice.iter().map(|x| x.to_string()).collect()
}

#[test]
fn test_empty_file_public() {
    let r = parse_tags::<String>(&[], "public_empty.md");
    assert_eq!(r, vec![]);
}

#[test]
fn test_single_valid_detail_block_public() {
    let lines = lines_str(&[
        "<details>",
        "<summary>This is a new public summary</summary>",
        "Public content goes here.",
        "</details>",
    ]);
    let result = parse_tags(&lines, "file_public.md");
    assert_eq!(result.len(), 1);
    let block = &result[0];
    assert_eq!(block["summary"], "This is a new public summary");
    assert_eq!(block["content"], "Public content goes here.");
    assert_eq!(block["start"], 0);
    assert_eq!(block["end"], 3);
    assert_eq!(block["filename"], "file_public.md");
}

#[test]
fn test_detail_block_missing_end_public() {
    let lines = lines_str(&[
        "<details>",
        "<summary>Public missing close</summary>",
        "Some content"
    ]);
    let result = parse_tags(&lines, "public_missingend.md");
    assert_eq!(result, vec![]);
}

#[test]
fn test_multiple_blocks_with_invalid_one_public() {
    let lines = lines_str(&[
        "<details>",
        "<summary>Block A</summary>",
        "Alpha content.",
        "</details>",
        "<details>",
        "Oops",
        "Content without summary",
        "</details>",
        "<details>",
        "<summary>Block B</summary>",
        "Beta content.",
        "</details>",
    ]);
    let result = parse_tags(&lines, "multi_public.md");
    assert_eq!(result.len(), 2);
    assert_eq!(result[0]["summary"], "Block A");
    assert_eq!(result[1]["summary"], "Block B");
}

#[test]
fn test_detail_block_with_content_public() {
    let lines = lines_str(&[
        "<details>",
        "<summary>Alternate summary</summary>",
        "First public line.",
        "Second public line.",
        "</details>",
    ]);
    let result = parse_tags(&lines, "cpublic.md");
    assert_eq!(result[0]["content"], "First public line.\nSecond public line.");
}

// Formatting checks
#[test]
fn test_valid_detail_format_public() {
    let tag = [
        ("summary".to_string(), "A public summary".into()),
        ("content".to_string(), "A content detail.".into()),
        ("start".to_string(), 20.into()),
        ("end".to_string(), 23.into()),
        ("filename".to_string(), "another_public.md".into()),
    ].iter().cloned().collect::<HashMap<_, _>>();
    let tags = vec![tag];
    let errors = check_formatting(&tags);
    assert_eq!(errors, vec![]);
}

#[test]
fn test_missing_summary_public() {
    let tag = [
        ("summary".to_string(), "".into()),
        ("content".to_string(), "Content that's public and missing summary.".into()),
        ("start".to_string(), 150.into()),
        ("end".to_string(), 159.into()),
        ("filename".to_string(), "no_public_summary.md".into()),
    ].iter().cloned().collect::<HashMap<_, _>>();
    let tags = vec![tag];
    let errors = check_formatting(&tags);
    assert!(errors.iter().any(|e| e.to_lowercase().contains("missing summary")));
}

#[test]
fn test_mismatched_tags_public() {
    let tag = [
        ("summary".to_string(), "public fail".into()),
        ("content".to_string(), "content".into()),
        ("start".to_string(), 9.into()),
        ("end".to_string(), serde_json::Value::Null),
        ("filename".to_string(), "badtag_public_2.md".into()),
    ].iter().cloned().collect::<HashMap<_, _>>();
    let tags = vec![tag];
    let errors = check_formatting(&tags);
    assert!(errors.iter().any(|e| {
        e.to_lowercase().contains("mismatched") || e.to_lowercase().contains("unterminated")
    }));
}