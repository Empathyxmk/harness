use flashtext::KeywordProcessor;

#[test]
fn test_list_loading() {
    let mut kp = KeywordProcessor::new();
    let keyword_list = vec!["java".to_string(), "product management".to_string()];
    kp.add_keywords_from_list(&keyword_list);
    let sentence = "I know java and product management";
    let mut extracted = kp.extract_keywords(sentence);
    extracted.sort();
    let mut expected = vec!["java".to_string(), "product management".to_string()];
    expected.sort();
    assert_eq!(extracted, expected);
    let sentence_new = kp.replace_keywords(sentence);
    assert_eq!(sentence_new, "I know java and product management");
}