use flashtext::KeywordProcessor;
use std::collections::HashMap;

#[test]
fn test_get_all_keywords() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("j2ee", "Java");
    kp.add_keyword("colour", "color");
    let mut expected = HashMap::new();
    expected.insert("colour".to_string(), "color".to_string());
    expected.insert("j2ee".to_string(), "Java".to_string());
    let out = kp.get_all_keywords();
    for (k, v) in expected {
        assert_eq!(out.get(&k).unwrap(), &v);
    }
}