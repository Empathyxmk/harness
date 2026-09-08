use crate::utils::is_ajax;
use std::collections::HashMap;
use crate::forms::SubscriberEmailForm;

#[test]
fn test_send_subscription_verification_email_logic() {
    // Simulated: check that get_verification_url returns expected url.
    let subscriber = crate::models::Subscriber::new(1, "test@test.com", false, false, None);
    let url = subscriber.get_verification_url();
    assert!(url.contains(&subscriber.token));
}

#[test]
fn test_send_newsletter_email_logic() {
    // Just check struct creation and "subject" field logic
    use chrono::Utc;
    let newsletter = crate::models::Newsletter::new(1, "Sample", false, Utc::now(), None);
    assert_eq!(newsletter.str_(), "Sample");
}

#[test]
fn test_is_ajax_true() {
    let mut headers = HashMap::new();
    headers.insert("X-Requested-With", "XMLHttpRequest");
    assert!(is_ajax(&headers));
}

#[test]
fn test_is_ajax_false() {
    let headers: HashMap<&str, &str> = HashMap::new();
    assert!(!is_ajax(&headers));
}

#[test]
fn test_form_valid() {
    let mut data = HashMap::new();
    data.insert("email_address", "user@test.com");
    let form = SubscriberEmailForm::new(Some(&data));
    assert!(form.is_valid());
    assert_eq!(
        form.email_address.as_ref().unwrap(),
        "user@test.com"
    );
}

#[test]
fn test_form_invalid() {
    let mut data = HashMap::new();
    data.insert("email_address", "invalid");
    let form = SubscriberEmailForm::new(Some(&data));
    assert!(!form.is_valid());
    assert!(form.errors().contains(&"email_address".to_string()));
}

#[test]
fn test_form_missing() {
    let form = SubscriberEmailForm::new(None);
    assert!(!form.is_valid());
    assert!(form.errors().contains(&"email_address".to_string()));
}