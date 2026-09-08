use flask_babel_rs::*;
use serial_test::serial;

#[test]
#[serial]
fn test_public_multiple_apps() {
    let mut b = Babel::new();

    let mut app1 = DummyApp::new();
    b.init_app(&mut app1, Some("fr_FR"));

    let mut app2 = DummyApp::new();
    b.init_app(&mut app2, Some("it_IT"));

    {
        let _locale_guard = b.force_locale("fr_FR");
        assert_eq!(get_locale(), "fr_FR");
        let mut map = std::collections::HashMap::new();
        map.insert("user", "Marie");
        assert_eq!(b.gettext("Welcome %(user)s!", Some(map)), "Welcome Marie!");
    }

    {
        let _locale_guard = b.force_locale("it_IT");
        assert_eq!(get_locale(), "it_IT");
        let mut map = std::collections::HashMap::new();
        map.insert("user", "Luca");
        assert_eq!(b.gettext("Welcome %(user)s!", Some(map)), "Welcome Luca!");
    }
}