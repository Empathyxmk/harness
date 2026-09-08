use flask_babel_rs::*;

#[test]
fn test_public_babel_with_app_factory() {
    fn create_app(_config: Option<&str>) -> DummyApp {
        let mut app = DummyApp::new();
        Babel::new().init_app(&mut app, Some("es"));
        app
    }

    let app = create_app(Some("es"));
    let _locale_guard = Babel::new().force_locale("es");
    assert_eq!(get_locale(), "es");
}

#[test]
fn test_public_babel_factory_deferred_init() {
    let created = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
    let cloned = created.clone();

    fn my_selector(cloned: std::sync::Arc<std::sync::Mutex<Vec<u32>>>) -> &'static str {
        cloned.lock().unwrap().push(100);
        "fr"
    }

    let mut b = Babel::new();
    let mut app = DummyApp::new();
    b.init_app(&mut app, Some(my_selector(cloned)));
    {
        let _locale_guard = b.force_locale("fr");
        assert_eq!(get_locale(), "fr");
        let collected = created.lock().unwrap();
        assert_eq!(*collected, vec![100]);
    }
}