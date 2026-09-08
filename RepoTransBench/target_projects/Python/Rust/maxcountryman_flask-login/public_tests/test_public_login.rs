#[cfg(test)]
mod tests {
    use crate::login_manager::*;

    #[test]
    fn test_instance_defaults_public() {
        let lm = LoginManager::new();
        assert!(lm.login_view.is_none());
        assert_eq!(lm.id_attribute, "get_id".to_owned());
        assert!(lm.login_message_category.contains("message"));
        assert!(lm.needs_refresh_message.to_lowercase().contains("refresh"));
        assert!({
            lm.session_protection.is_none() ||
            lm.session_protection == Some("basic".to_owned()) ||
            lm.session_protection == Some("strong".to_owned())
        });
        assert!(lm.anonymous_user() == "AnonymousUser".to_owned());
    }

    #[test]
    fn test_login_manager_custom_values_public() {
        let mut lm = LoginManager::new();
        lm.login_view = Some("/custom_login".to_string());
        lm.refresh_view = Some("/refresh_needed".to_string());
        lm.login_message = "You must sign in!".to_string();
        lm.blueprint_login_views.insert("bp2".into(), "/bp2_custom_login".into());
        assert!(lm.login_view.as_ref().unwrap().starts_with('/'));
        assert!(lm.refresh_view.as_ref().unwrap().ends_with("needed"));
        assert!(lm.login_message.contains("sign in"));
        assert!(lm.blueprint_login_views.get("bp2").unwrap().starts_with("/bp2"));
        lm.session_protection = Some("strong".to_string());
        assert_eq!(lm.session_protection.as_deref(), Some("strong"));
    }

    #[test]
    fn test_login_manager_anonymous_user_public() {
        let mut lm = LoginManager::new();
        // Overwrite anonymous_user function
        lm.anonymous_user = std::sync::Arc::new(|| "CustomAnon".to_string());
        let res = (lm.anonymous_user)();
        assert_eq!(res, "CustomAnon");
    }

    #[test]
    fn test_localize_callback_public() {
        let mut lm = LoginManager::new();
        use std::sync::{Arc, Mutex};
        let val = Arc::new(Mutex::new(String::new()));
        let val_clone = val.clone();
        lm.localize_callback = Some(Arc::new(move |txt| {
            *val_clone.lock().unwrap() = txt.to_string();
            txt.to_string()
        }));
        if let Some(cb) = &lm.localize_callback {
            cb("hello");
        }
        assert_eq!(&*val.lock().unwrap(), "hello");
    }
}