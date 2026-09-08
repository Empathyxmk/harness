use flashtext::KeywordProcessor;

#[test]
fn test_public_extract_deletion() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("skype", "messenger");
    let sentence = "hello, do you have skpe ?";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("messenger"));
}

#[test]
fn test_public_replace_addition() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("colour here", "couleur ici");
    kp.add_keyword("and heere", "et ici");
    let sentence = "color here blabla and here";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("couleur ici") || replaced.contains("et ici"));
}

#[test]
fn test_public_replace_multiple_keywords() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("first keyword", "1st keyword");
    kp.add_keyword("second keyword", "2nd keyword");
    let sentence = "start with a first kyword then add a secand keyword";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("1st keyword"));
    assert!(replaced.contains("2nd keyword"));
}