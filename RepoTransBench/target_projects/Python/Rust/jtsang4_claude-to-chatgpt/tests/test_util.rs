use claude_to_chatgpt::util;

#[test]
fn test_num_tokens_from_string_basic() {
    assert_eq!(util::num_tokens_from_string("abc"), 3);
}

#[test]
fn test_num_tokens_from_string_empty() {
    assert_eq!(util::num_tokens_from_string(""), 0);
}