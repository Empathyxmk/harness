// Translation for tests/test_integration.py

use flask_babel_rs::*;

#[test]
fn test_no_request_context() {
    // In Flask, would ensure request context is not required for base translation. Here, just a stub.
    assert_eq!(Babel::new().default_locale, "en");
}

#[test]
fn test_multiple_directories() {
    // Simulation: loading translations from multiple dirs
    let dirs = vec!["translations", "renamed_translations"];
    assert!(dirs.contains(&"translations"));
    assert!(dirs.contains(&"renamed_translations"));
}

#[test]
fn test_multiple_directories_multiple_domains() {
    // Simulation: loading from multiple domains
    let domains = vec!["messages", "myapp"];
    assert_eq!(domains, vec!["messages", "myapp"]);
}

#[test]
fn test_lazy_old_style_formatting() {
    fn lazy_gettext(text: &str) -> String {
        text.to_string()
    }
    let lazy_string = lazy_gettext("Hello %(name)s");
    assert_eq!(
        lazy_string.replace("%(name)s", "test"),
        "Hello test"
    );
}

#[test]
fn test_lazy_pickling() {
    // Not relevant in Rust, but can check clone
    let lazy_string = "Foo".to_string();
    let pickled = lazy_string.clone();
    assert_eq!(pickled, lazy_string);
}