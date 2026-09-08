use flask_babel_rs::*;
use serial_test::serial;

#[test]
#[serial]
fn test_multiple_apps() {
    let mut b = Babel::new();

    let mut app1 = DummyApp::new();
    b.init_app(&mut app1, Some("de_DE"));

    let mut app2 = DummyApp::new();
    b.init_app(&mut app2, Some("en_US"));

    {
        let _locale_guard = b.force_locale("de_DE");
        assert_eq!(get_locale(), "de_DE");
        let mut map = std::collections::HashMap::new();
        map.insert("name", "Peter");
        assert_eq!(b.gettext("Hello %(name)s!", Some(map.clone())), "Hello Peter!");
    }

    {
        let _locale_guard = b.force_locale("en_US");
        assert_eq!(get_locale(), "en_US");
        let mut map = std::collections::HashMap::new();
        map.insert("name", "Peter");
        assert_eq!(
            b.gettext("Hello %(name)s!", Some(map.clone())),
            "Hello Peter!"
        );
    }
}