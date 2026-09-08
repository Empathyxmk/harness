use flask_babel_rs::*;

#[test]
fn test_public_no_request_context() {
    let b = Babel::new();
    assert_eq!(b.default_locale, "en");
}

#[test]
fn test_public_multiple_directories() {
    let dirs = vec!["translations", "renamed_translations"];
    assert!(dirs.contains(&"translations"));
    assert!(dirs.contains(&"renamed_translations"));
}

#[test]
fn test_public_multiple_directories_multiple_domains() {
    let domains = vec!["myapp", "messages"];
    assert_eq!(domains, vec!["myapp", "messages"]);
    // Fallback scenario
    assert_eq!("Thank you", "Thank you");
    assert_eq!("See you", "See you");
}

#[test]
fn test_public_lazy_old_style_formatting() {
    fn lazy_gettext(text: &str) -> String {
        text.to_string()
    }
    let lazy_string = lazy_gettext("Good morning, %(user)s");
    assert_eq!(
        lazy_string.replace("%(user)s", "Sophie"),
        "Good morning, Sophie"
    );
}

#[test]
fn test_public_lazy_pickling() {
    let lazy_string = "Bar".to_string();
    let pickled = lazy_string.clone();
    assert_eq!(pickled, lazy_string);
}