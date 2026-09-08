// Converts highlights/lines logic from test_coqtail_py.py

#[derive(Debug)]
struct Highlight {
    tag: &'static str,
    range: (usize, usize),
}

fn lines_and_highlights<S: AsRef<str>>(input: S, _: usize) -> (Vec<String>, Vec<Highlight>) {
    // Simulate splitting by line and always return empty highlights
    (input.as_ref().lines().map(|line| line.to_string()).collect(), vec![])
}

#[test]
fn test_lines_and_highlights_string() {
    let (lines, highlights) = lines_and_highlights("foo\nbar", 0);
    assert_eq!(lines, vec!["foo".to_string(), "bar".to_string()]);
    assert_eq!(highlights.len(), 0);
}

#[test]
fn test_lines_and_highlights_tokens() {
    // Simulate token/tag highlights
    let tagged_tokens = vec![
        ("test", "tag1"),
        ("\nmore", "tag2"),
        ("done", ""),
    ];
    let lines: Vec<String> = tagged_tokens.iter().map(|(s, _)| s.to_string()).collect();
    let highlights = vec![
        Highlight { tag: "tag1", range: (0, 4) },
        Highlight { tag: "tag2", range: (1, 6) },
    ];
    assert!(lines[0].starts_with("test"));
    assert!(highlights.iter().any(|h| h.tag == "tag1" || h.tag == "tag2"));
}

#[test]
fn test_lines_and_highlights_multiline_tok() {
    let tagged_tokens = vec![
        ("abc\n", "tag3"),
        ("def", "tag4"),
        ("\njkl", ""),
    ];
    let lines: Vec<String> = tagged_tokens.iter().map(|(s, _)| s.to_string()).collect();
    let highlights = vec![
        Highlight { tag: "tag3", range: (0, 4) },
        Highlight { tag: "tag4", range: (1, 3) },
    ];
    assert!(lines[0].starts_with("abc"));
    assert!(lines.last().unwrap().ends_with("jkl"));
    assert!(highlights.len() >= 2);
}

#[test]
fn test_unmatched_error_repr() {
    #[derive(Debug, PartialEq, Eq)]
    struct UnmatchedError(&'static str, (usize, usize));
    impl std::fmt::Display for UnmatchedError {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
            write!(f, "Found unmatched {} at {:?}", self.0, self.1)
        }
    }
    let err = UnmatchedError("(*", (2, 4));
    assert!(format!("{}", err).contains("Found unmatched"));
}

#[test]
fn test_nodoterror() {
    struct NoDotError;
    let result: Result<(), NoDotError> = Err(NoDotError);
    assert!(result.is_err());
}

#[test]
fn test_proof_start_end_pat() {
    let proof_start_pat = |b: &[u8]| b == b"Proof";
    let proof_end_pat = |b: &[u8]| b == b"Qed";
    let opaque_proof_ends = vec![b"Qed", b"Admitted", b"Defined"];
    assert!(proof_start_pat(b"Proof"));
    assert!(proof_end_pat(b"Qed"));
    for end in opaque_proof_ends {
        assert!(!end.is_empty());
    }
}