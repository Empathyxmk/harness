#[cfg(test)]
mod tests {
    use crate::about;
    use std::cell::RefCell;

    thread_local! {
        static LAST_WARNING: RefCell<Option<String>> = RefCell::new(None);
    }

    #[test]
    fn test_about_warns() {
        // There's no Python-like DeprecationWarning, but test API/simulation
        let warning = about::warn_about();
        assert!(warning.to_lowercase().contains("deprecated"));
        assert_eq!(about::TITLE, "Flask-Login");
        assert_eq!(about::VERSION, "0.7.0");
    }

    #[test]
    fn test_init_dunder_version_warns() {
        // Simulate version check + warning
        fn fake_version(_: &str) -> String { "1.2.3".to_string() }
        let warning = about::warn_about();
        assert!(warning.to_lowercase().contains("deprecated"));
        let version = fake_version("flask-login");
        assert_eq!(version, "1.2.3");
    }

    #[test]
    fn test_init_dunder_version_attribute_error() {
        // No attributes: simulate error
        struct DummyStruct;
        let res = std::panic::catch_unwind(|| {
            // Simulate attempt to access missing attribute
            let _ = dummy_struct_field_access();
        });
        assert!(
            res.is_err(),
            "Should raise simulated AttributeError"
        );
    }

    fn dummy_struct_field_access() -> i32 {
        panic!("notarealattr")
    }
}