use flashtext::KeywordProcessor;
use std::fs;

#[test]
fn test_file_format_one() {
    let mut keyword_processor = KeywordProcessor::new();
    // We'll load file "testdata/keywords_format_one.txt"
    let file_content = fs::read_to_string("testdata/keywords_format_one.txt")
        .expect("Could not open keywords_format_one.txt");
    for line in file_content.lines() {
        // Assume each line is comma separated
        let mut parts = line.split(',');
        if let (Some(keyword), Some(clean)) = (parts.next(), parts.next()) {
            keyword_processor.add_keyword(keyword, clean);
        }
    }
    let sentence = "I know java_2e and product management techniques";
    let mut keywords_extracted = keyword_processor.extract_keywords(sentence);
    keywords_extracted.sort();
    let mut expected = vec!["java".to_string(), "product management".to_string()];
    expected.sort();
    assert_eq!(keywords_extracted, expected);

    let sentence_new = keyword_processor.replace_keywords(sentence);
    assert_eq!(sentence_new, "I know java and product management");
}

#[test]
fn test_file_format_two() {
    let mut keyword_processor = KeywordProcessor::new();
    let file_content = fs::read_to_string("testdata/keywords_format_two.txt")
        .expect("Could not open keywords_format_two.txt");
    for line in file_content.lines() {
        // Split by comma, could add more format parsers if needed.
        let mut parts = line.split(',');
        if let (Some(keyword), Some(clean)) = (parts.next(), parts.next()) {
            keyword_processor.add_keyword(keyword, clean);
        }
    }
    let sentence = "I know java and product management";
    let mut keywords_extracted = keyword_processor.extract_keywords(sentence);
    keywords_extracted.sort();
    let mut expected = vec!["java".to_string(), "product management".to_string()];
    expected.sort();
    assert_eq!(keywords_extracted, expected);

    let sentence_new = keyword_processor.replace_keywords(sentence);
    assert_eq!(sentence_new, "I know java and product management");
}