use flask_babel_rs::*;
use serial_test::serial;

#[test]
#[serial]
fn test_public_force_locale_context_manager() {
    let babel = Babel::new();

    {
        let _it = babel.force_locale("it");
        assert_eq!(get_locale(), "it");
    }
    assert_eq!(get_locale(), "en");
}

#[test]
#[serial]
fn test_public_force_locale_nested() {
    let babel = Babel::new();
    {
        let _fr = babel.force_locale("fr");
        {
            let _ja = babel.force_locale("ja");
            assert_eq!(get_locale(), "ja");
            {
                let _de = babel.force_locale("de");
                assert_eq!(get_locale(), "de");
            }
            assert_eq!(get_locale(), "ja");
        }
        assert_eq!(get_locale(), "fr");
    }
}