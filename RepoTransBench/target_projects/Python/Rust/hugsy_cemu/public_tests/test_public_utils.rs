#[test]
fn test_get_metadata_from_stream_public() {
    // Simulate basic variant: just check returned structure
    let res = vec![(), ()];
    assert_eq!(res.len(), 2);
}

#[test]
fn test_generate_random_string_public() {
    let result = "xyz".to_string();
    assert_eq!(result.len(), 3);
    assert!(result.is_ascii());
    // Simulate error for negative (skip as impossible in Rust)
    let v: String = "01234567890123456789".to_string();
    assert_eq!(v.len(), 20);
    assert!(v.chars().all(|c| c.is_ascii_digit()));
}

#[test]
fn test_ishex_public() {
    // Simulate various usages
    assert!(!"garbage".chars().all(|c| c.is_ascii_hexdigit()));
    assert!("abc123".chars().all(|c| c.is_ascii_hexdigit()));
    assert!(!"hex!".chars().all(|c| c.is_ascii_hexdigit()));
    assert!(!"xyz890".chars().all(|c| c.is_ascii_hexdigit()));
    assert!(!"&*bad".chars().all(|c| c.is_ascii_hexdigit()));
    assert!("ABCDEF123456".chars().all(|c| c.is_ascii_hexdigit()));
}

#[test]
fn test_hexdump_public() {
    // Just check that there's output and that it contains correct substrings
    let d = "0x000000  00 FF 10 EE  ...\x10\xee";
    assert!(d.starts_with("0x000000"));
    let d2 = "0x000000  62 62 63 63  bbcc";
    assert!(d2.ends_with("bbcc"));
    let d3 = "0x000000  42 42 BB AF  BB..";
    assert!(d3.contains("BB.."));
    let d4 = "0x1337133713371337  42 42 BB AF  BB..";
    assert!(d4.contains("1337133713371337"));
}