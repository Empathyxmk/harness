// Translation of uuslug/tests/test_models_integration.py to Rust

use crate::models::{CoolSlug, AnotherSlug, TruncatedSlug};

#[test]
fn test_cool_slug_model_save() {
    let mut obj = CoolSlug::new("Django Is Great!");
    obj.save();
    assert!(obj.slug.contains("django-is-great"));
}

#[test]
fn test_another_slug_model_save() {
    let mut obj = AnotherSlug::new("Unique Name For Slug");
    obj.save();
    assert!(obj.slug.starts_with("unique-name-for-slug"));
}

#[test]
fn test_truncated_slug_save() {
    let mut obj = TruncatedSlug::new("321 short truncate slug name");
    obj.save();
    assert!(obj.slug.len() <= 17);
}