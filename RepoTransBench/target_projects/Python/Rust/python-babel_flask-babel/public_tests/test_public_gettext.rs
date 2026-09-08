use flask_babel_rs::*;

#[test]
fn test_public_basic_translation() {
    let mut b = Babel::new();
    b.default_locale = "ja".to_string();
    {
        let _locale_guard = b.force_locale("ja");
        let mut map = std::collections::HashMap::new();
        map.insert("name", "Taro");
        let rv = b.gettext("Hi %(name)s!", Some(map));
        assert!(rv.contains("Taro"));
    }
}

#[test]
fn test_public_ngettext() {
    let mut b = Babel::new();
    b.default_locale = "de_DE".to_string();
    let mut map = std::collections::HashMap::new();
    map.insert("num", "1");
    let rv_sing = b.gettext("There is %(num)d mouse", Some(map.clone()));
    assert!(rv_sing.contains("mouse"));
    map.insert("num", "5");
    let rv_plur = b.gettext("There are %(num)d mice", Some(map.clone()));
    assert!(rv_plur.contains("mice"));
}

#[test]
fn test_public_lazy_gettext() {
    struct LazyString {
        s: String,
    }
    impl std::fmt::Display for LazyString {
        fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
            write!(f, "{}", self.s)
        }
    }
    let s = LazyString {
        s: "Welcome, Kenta!".to_string(),
    };
    assert!(format!("{}", s).contains("Kenta"));
}

#[test]
fn test_public_gettext_with_domain() {
    let mut b = Babel::new();
    b.domain = "myapp".to_string();
    b.default_locale = "de_DE".to_string();
    let val = b.gettext("Good night", None);
    assert!(val.contains("Good"));
}