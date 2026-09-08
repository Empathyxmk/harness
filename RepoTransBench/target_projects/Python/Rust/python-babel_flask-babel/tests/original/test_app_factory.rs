use flask_babel_rs::*;

#[test]
fn test_app_factory() {
    let mut b = Babel::new();

    fn locale_selector() -> &'static str {
        "de_DE"
    }

    let mut app = DummyApp::new();
    b.init_app(&mut app, Some("en_US"));
    {
        let _locale_guard = b.force_locale(locale_selector());
        let mut map = std::collections::HashMap::new();
        map.insert("name", "Peter");
        assert_eq!(b.gettext("Hello %(name)s!", Some(map)), "Hello Peter!");
    }
}