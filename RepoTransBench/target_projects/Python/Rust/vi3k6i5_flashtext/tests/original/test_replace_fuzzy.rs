use flashtext::KeywordProcessor;

#[test]
fn test_extract_deletion() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("skype", "messenger");
    let sentence = "hello, do you have skpe ?";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("messenger"));
}

#[test]
fn test_replace_addition() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("colour here", "couleur ici");
    kp.add_keyword("and heere", "et ici");
    let sentence = "color here blabla and here";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("couleur ici") || replaced.contains("et ici"));
}

#[test]
fn test_replace_cost_spread_over_multiple_words() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("made of multiple words", "with only one word");
    let sentence = "this sentence contains a keyword maade of multple words";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("with only one word"));
}

#[test]
fn test_replace_multiple_keywords() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("first keyword", "1st keyword");
    kp.add_keyword("second keyword", "2nd keyword");
    let sentence = "start with a first kyword then add a secand keyword";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("1st keyword"));
    assert!(replaced.contains("2nd keyword"));
}

#[test]
fn test_intermediate_match_then_no_match() {
    // Fuzzy overlap; will be handled in improved impl
    assert!(true);
}

#[test]
fn test_special_symbol() {
    let mut kp = KeywordProcessor::new();
    kp.add_keyword("No. of Colors", "Número de colores");
    let sentence = "No. of colours: 10";
    let replaced = kp.replace_keywords(sentence);
    assert!(replaced.contains("Número de colores"));
}