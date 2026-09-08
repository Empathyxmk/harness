use flask_babel_rs::*;

struct DummyApp {
    config: std::collections::HashMap<String, String>,
    extensions: std::collections::HashMap<String, BabelConfiguration>,
}
impl DummyApp {
    fn new() -> Self {
        DummyApp {
            config: std::collections::HashMap::new(),
            extensions: std::collections::HashMap::new(),
        }
    }
}

#[test]
fn test_public_babel_init_and_app_properties() {
    let mut app = DummyApp::new();
    let mut babel = Babel::new();
    babel.init_app(&mut app, None);
    let config = app.extensions.get("babel").unwrap();
    assert_eq!(config.default_locale, "en");
    assert_eq!(config.default_domain, "messages");
}

#[test]
fn test_public_babel_init_app_config_options_override() {
    let mut app = DummyApp::new();
    app.config.insert("BABEL_DEFAULT_LOCALE".to_string(), "es".to_string());
    app.config
        .insert("BABEL_DOMAIN".to_string(), "alt_domain".to_string());
    app.config
        .insert("BABEL_TRANSLATION_DIRECTORIES".to_string(), "alpha;beta".to_string());
    let mut babel = Babel::new();
    babel.init_app(&mut app, Some("es"));
    let config = app.extensions.get("babel").unwrap();
    assert_eq!(config.default_locale, "es");
}

#[test]
fn test_public_babel_init_app_with_selectors() {
    let mut app = DummyApp::new();
    let mut babel = Babel::new();
    let _selector = || "it";
    babel.init_app(&mut app, Some("it"));
    let config = app.extensions.get("babel").unwrap();
    assert_eq!(config.default_locale, "it");
}

#[test]
fn test_public_default_date_formats_defined() {
    let _babel = Babel::new();
    assert_eq!("en", Babel::new().default_locale);
}