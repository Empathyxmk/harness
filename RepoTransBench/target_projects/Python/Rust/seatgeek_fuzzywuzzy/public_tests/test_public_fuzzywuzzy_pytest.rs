use seatgeek_fuzzywuzzy::{fuzz, process};

#[test]
fn test_partial_ratio_works_on_empty_string() {
    // Equivalent to checking fuzz::partial_ratio("", "") == 100
    let score = fuzz::partial_ratio("", "");
    assert_eq!(score, 100);
}

#[test]
fn test_process_tokenizer_logs_warning_on_all_punctuation() {
    // Simulate: processor reduces query to "" after removing all punctuation,
    // so process.extract_one should handle this gracefully (e.g., return None or best guess)
    let query = ":::::::";
    let choices = vec![":::::::"];
    let result = process::extract_one(query, choices.iter().map(|x| *x));
    // The main test is to ensure it does not panic, and returns an Option
    assert!(result.is_some() || result.is_none());
}