use flashtext::KeywordProcessor;

#[test]
fn test_term_in_dictionary() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("j2ee", "Java");
    kp.add_keyword("colour", "color");
    assert_eq!(kp.get_keyword("j2ee"), Some(&"Java".to_string()));
    assert_eq!(kp.get_keyword("colour"), Some(&"color".to_string()));
    assert_eq!(kp.get_keyword("Test"), None);
    assert!(kp.get_all_keywords().contains_key("colour"));
    assert!(!kp.get_all_keywords().contains_key("Test"));
}

#[test]
fn test_term_in_dictionary_case_sensitive() {
    let mut kp = KeywordProcessor::new_case(true);
    kp.add_keyword("j2ee", "Java");
    kp.add_keyword("colour", "color");
    assert_eq!(kp.get_keyword("j2ee"), Some(&"Java".to_string()));
    assert_eq!(kp.get_keyword("colour"), Some(&"color".to_string()));
    assert_eq!(kp.get_keyword("J2ee"), None);
    assert!(kp.get_all_keywords().contains_key("colour"));
    assert!(!kp.get_all_keywords().contains_key("Colour"));
}