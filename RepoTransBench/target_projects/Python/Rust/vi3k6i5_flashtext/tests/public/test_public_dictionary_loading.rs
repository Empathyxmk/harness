use std::collections::HashMap;
use flashtext::KeywordProcessor;

#[test]
fn test_public_dictionary_loading() {
    let mut keyword_processor = KeywordProcessor::new();
    let mut keyword_dict = HashMap::new();
    keyword_dict.insert(
        "java".to_string(),
        vec!["java_2e".to_string(), "java programing".to_string()],
    );
    keyword_dict.insert(
        "product management".to_string(),
        vec![
            "product management techniques".to_string(),
            "product management".to_string(),
        ],
    );
    keyword_processor.add_keywords_from_dict(&keyword_dict);

    let sentence = "I know java_2e and product management techniques";
    let mut keywords_extracted = keyword_processor.extract_keywords(sentence);
    keywords_extracted.sort();
    let mut expected = vec!["java".to_string(), "product management".to_string()];
    expected.sort();
    assert_eq!(keywords_extracted, expected);

    let sentence_new = keyword_processor.replace_keywords(sentence);
    assert_eq!(
        sentence_new,
        "I know java and product management"
    );
}