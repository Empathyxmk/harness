use flashtext::KeywordProcessor;

#[test]
#[should_panic]
fn test_public_iterator_not_implemented_error() {
    panic!("NotImplementedError: KeywordProcessor is not directly iterable");
}

#[test]
fn test_public_empty_string() {
    let kp = KeywordProcessor::new();
    assert_eq!(kp.extract_keywords(""), Vec::<String>::new());
    assert_eq!(kp.replace_keywords(""), "");
}