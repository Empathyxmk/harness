use crate::forms::SubscriberEmailForm;
use std::collections::HashMap;

#[test]
fn test_valid_email() {
    let mut data = HashMap::new();
    data.insert("email_address", "test@example.com");
    let form = SubscriberEmailForm::new(Some(&data));
    assert!(form.is_valid());
    assert_eq!(form.email_address.as_ref().unwrap(), "test@example.com");
}

#[test]
fn test_invalid_email() {
    let mut data = HashMap::new();
    data.insert("email_address", "not-an-email");
    let form = SubscriberEmailForm::new(Some(&data));
    assert!(!form.is_valid());
    assert!(form.errors().contains(&"email_address".to_string()));
}

#[test]
fn test_missing_email() {
    let form = SubscriberEmailForm::new(None);
    assert!(!form.is_valid());
    assert!(form.errors().contains(&"email_address".to_string()));
}