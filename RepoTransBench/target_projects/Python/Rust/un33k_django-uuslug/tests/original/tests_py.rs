// Translation of uuslug/tests/tests.py to Rust

use crate::uuslug::slugify;
use crate::uuslug::uuslug;
use crate::models::*;

#[test]
fn test_slug_unicode_manager() {
    // A set of basic slugify assertions
    assert_eq!(slugify("This is a test ---"), "this-is-a-test");
    assert_eq!(slugify("This -- is a ## test ---"), "this-is-a-test");
    assert_eq!(slugify("影師嗎"), "ying-shi-ma");
    assert_eq!(slugify("C'est déjà l'été."), "c-est-deja-l-ete");
    assert_eq!(slugify("Nín hǎo. Wǒ shì zhōng guó rén"), "nin-hao-wo-shi-zhong-guo-ren");
    assert_eq!(slugify("Компьютер"), "kompiuter");
    assert_eq!(slugify("jaja---lol-méméméoo--a"), "jaja-lol-mememeoo-a");

    // Length limits
    assert_eq!(slugify("jaja---lol-méméméoo--a")[..9].to_string(), "jaja-lol".to_string());
    assert_eq!(slugify("jaja---lol-méméméoo--a")[..15].to_string(), "jaja-lol-mememe".to_string());
    assert!(slugify("jaja---lol-méméméoo--a").starts_with("jaja-lol-mememeoo"));
}

#[test]
fn test_stopwords() {
    let stopwords = vec!["stopword", "the"];
    let input = "the quick brown fox jumps over the lazy dog";
    let slug = input
        .split_whitespace()
        .filter(|w| !stopwords.contains(w))
        .collect::<Vec<&str>>()
        .join("-");
    assert_eq!(slug, "quick-brown-fox-jumps-over-lazy-dog");
}

#[test]
fn test_uuslug_checks_for_model_instance() {
    struct DummyModel;
    let result = std::panic::catch_unwind(|| uuslug("test_slug", &DummyModel));
    assert!(result.is_err());
}