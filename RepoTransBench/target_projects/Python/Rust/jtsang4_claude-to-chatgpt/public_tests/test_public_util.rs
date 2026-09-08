use claude_to_chatgpt::util;

#[test]
fn test_public_num_tokens_from_string_nonempty() {
    assert_eq!(util::num_tokens_from_string("hello"), 5);
}

#[test]
fn test_public_num_tokens_from_string_empty() {
    assert_eq!(util::num_tokens_from_string(""), 0);
}