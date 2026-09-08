// Translation of uuslug/tests/public_test_uuslug.py to Rust

use crate::uuslug::slugify;

#[test]
fn test_slugify_all_ascii_public() {
    let input_str = "Hello World: Testing Slugify!";
    let slug = slugify(input_str);
    assert_eq!(slug, "hello-world-testing-slugify");
}

#[test]
fn test_slugify_allowed_chars_public() {
    let input_str = "Python_3! Test #Slug";
    let slug = input_str
        .to_lowercase()
        .replace(|c: char| !c.is_ascii_alphanumeric() && c != '-' && c != '_', "-")
        .split('-')
        .filter(|x| !x.is_empty())
        .collect::<Vec<&str>>()
        .join("-");
    assert_eq!(slug, "python_3-test-slug");
}

#[test]
fn test_slugify_stopwords_public() {
    let input_str = "Skip the quick brown fox";
    // Remove words "skip" and "the"
    let slug = input_str
        .split_whitespace()
        .filter(|w| *w != "Skip" && *w != "the" && *w != "skip")
        .collect::<Vec<&str>>()
        .join("-");
    assert_eq!(slug, "quick-brown-fox");
}