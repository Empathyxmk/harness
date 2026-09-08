// Rust translation of public test for check_vcs_permalinks

use tempfile::TempDir;

#[test]
fn test_get_pattern_matches_other_branch() {
    let newbranch = b"https://github.com/hello/world/blob/dev/file.py#L42";
    let hash_url = b"https://github.com/hello/world/blob/abc123de/file.py#L10";
    let bitbucket = b"https://bitbucket.org/foo/bar/src/master/file.py#lines-5";
    let non_github = b"https://gitlab.com/foo/bar/blob/master/file.py#L3";

    let pattern = get_pattern("github.com");
    assert!(pattern.is_match(newbranch));
    assert!(!pattern.is_match(hash_url));
    assert!(!pattern.is_match(bitbucket));
    assert!(!pattern.is_match(non_github));
}

fn get_pattern(_domain: &str) -> regex::Regex {
    regex::Regex::new(".*").unwrap()
}

// Implement further needed tests for filename detection etc.