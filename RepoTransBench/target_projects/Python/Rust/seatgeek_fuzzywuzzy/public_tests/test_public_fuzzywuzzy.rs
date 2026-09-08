use seatgeek_fuzzywuzzy::fuzz;

#[test]
fn test_ratio_basic_similarity() {
    assert_eq!(fuzz::ratio("this is a test", "this is a test"), 100);
    assert!(fuzz::ratio("fuzzy", "wuzzy") < 100);
    assert_eq!(fuzz::ratio("", ""), 100);
    assert_eq!(fuzz::ratio("", "hello"), 0);
}

#[test]
fn test_partial_ratio_similarity() {
    assert_eq!(fuzz::partial_ratio("test", "this is a test"), 100);
    assert!(fuzz::partial_ratio("partial", "ratio") < 100);
    assert_eq!(fuzz::partial_ratio("", ""), 100);
}

#[test]
fn test_token_sort_ratio() {
    assert_eq!(fuzz::token_sort_ratio("a b c", "b a c"), 100);
    assert!(fuzz::token_sort_ratio("apple", "banana") < 100);
}

#[test]
fn test_token_set_ratio() {
    assert_eq!(fuzz::token_set_ratio("a b c", "b a d"), 86); // Expect ~86 for 2/3 shared
    assert_eq!(fuzz::token_set_ratio("", ""), 100);
}