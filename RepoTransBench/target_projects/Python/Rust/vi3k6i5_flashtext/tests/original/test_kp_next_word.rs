use flashtext::KeywordProcessor;

#[test]
fn test_next_word() {
    let mut kp = KeywordProcessor::new();
    assert_eq!(kp.get_next_word(""), "");
    assert_eq!(kp.get_next_word("random sentence"), "random");
    assert_eq!(kp.get_next_word(" random sentence"), "");
}