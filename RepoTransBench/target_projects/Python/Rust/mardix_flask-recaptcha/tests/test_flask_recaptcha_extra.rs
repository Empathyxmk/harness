// tests/test_flask_recaptcha_extra.rs

use std::collections::HashMap;

// Dummy App struct to mimic a Flask-like app
struct App {
    context: HashMap<String, String>,
}

impl App {
    fn new() -> Self {
        App {
            context: HashMap::new(),
        }
    }

    fn config(&self) -> &Self {
        self
    }

    fn configure(&mut self, key: &str, value: &str) {
        self.context.insert(key.to_string(), value.to_string());
    }

    fn get(&self, key: &str) -> Option<&String> {
        self.context.get(key)
    }

    fn context_processor<F>(&mut self, _fn: F)
    where
        F: Fn(),
    {
        // Dummy method for compatibility, does nothing in this stub
    }
}

// Dummy ReCaptcha struct to mimic Flask-Recaptcha functionality
#[derive(Default)]
struct ReCaptcha {
    site_key: Option<String>,
    secret_key: Option<String>,
    is_enabled: bool,
}

impl ReCaptcha {
    fn init(&mut self, app: &mut App) {
        if let (Some(site_key), Some(secret_key)) = (self.site_key.as_ref(), self.secret_key.as_ref()) {
            app.configure("RECAPTCHA_SITE_KEY", site_key);
            app.configure("RECAPTCHA_SECRET_KEY", secret_key);
            app.configure("RECAPTCHA_ENABLED", "true");
            self.is_enabled = true;
        } else {
            app.configure("RECAPTCHA_ENABLED", "false");
            self.is_enabled = false;
        }
    }

    fn get_code(&self) -> &'static str {
        if self.is_enabled {
            "<div>Recaptcha Widget HTML</div>"
        } else {
            ""
        }
    }
}

// The actual test functions
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_recaptcha_extra_configures_app_with_keys() {
        let mut app = App::new();
        let mut r = ReCaptcha {
            site_key: Some("1234".into()),
            secret_key: Some("abcd".into()),
            ..Default::default()
        };

        r.init(&mut app);

        assert_eq!(app.get("RECAPTCHA_SITE_KEY"), Some(&"1234".to_string()));
        assert_eq!(app.get("RECAPTCHA_SECRET_KEY"), Some(&"abcd".to_string()));
        assert_eq!(app.get("RECAPTCHA_ENABLED"), Some(&"true".to_string()));
        assert_eq!(r.get_code(), "<div>Recaptcha Widget HTML</div>");
    }

    #[test]
    fn test_recaptcha_extra_disabled_without_keys() {
        let mut app = App::new();
        let mut r = ReCaptcha::default();

        r.init(&mut app);

        assert_eq!(app.get("RECAPTCHA_ENABLED"), Some(&"false".to_string()));
        assert_eq!(r.get_code(), "");
    }

    #[test]
    fn test_context_processor_stub_is_callable() {
        let mut app = App::new();
        app.context_processor(|| {
            // Should execute without errors
        });
    }
}