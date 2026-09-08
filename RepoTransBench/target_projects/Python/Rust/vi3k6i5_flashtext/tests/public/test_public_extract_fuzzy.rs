use flashtext::KeywordProcessor;

#[test]
fn test_public_extract_deletion() {
    let mut keyword_proc = KeywordProcessor::new();
    keyword_proc.add_keyword("skype", "messenger");
    let sentence = "hello, do you have skpe ?";
    let extracted_keywords = keyword_proc.extract_keywords(sentence);
    assert_eq!(
        extracted_keywords,
        vec!["messenger".to_string()]
    );
}

#[test]
fn test_public_extract_addition() {
    let mut keyword_proc = KeywordProcessor::new();
    keyword_proc.add_keyword("colour here", "couleur ici");
    keyword_proc.add_keyword("and heere", "et ici");
    let sentence = "color here blabla and here";
    let expected = vec!["couleur ici".to_string(), "et ici".to_string()];
    let mut got = keyword_proc.extract_keywords(sentence);
    got.sort();
    let mut expected_sorted = expected.clone();
    expected_sorted.sort();
    assert_eq!(got, expected_sorted);
}

#[test]
fn test_public_extract_multiple_keywords() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("first keyword", "first keyword");
    kp.add_keyword("second keyword", "second keyword");
    let sentence = "starts with a first kyword then add a secand keyword";
    let mut out = kp.extract_keywords(sentence);
    out.sort();
    let mut expected = vec!["first keyword".to_string(), "second keyword".to_string()];
    expected.sort();
    assert_eq!(out, expected);
}