// Translation of uuslug/tests/public_test_models_integration.py to Rust

use crate::models::{CoolSlug, AnotherSlug, TruncatedSlug};

#[test]
fn test_cool_slug_model_save_public() {
    let mut obj = CoolSlug::new("Awesome Python Tooling!");
    obj.save();
    assert!(obj.slug.contains("awesome-python-tooling"));
}

#[test]
fn test_another_slug_model_save_public() {
    let mut obj = AnotherSlug::new("Distinct Slug Value");
    obj.save();
    assert!(obj.slug.starts_with("distinct-slug-value"));
}

#[test]
fn test_truncated_slug_save_public() {
    let mut obj = TruncatedSlug::new("987 extra long truncated slug example");
    obj.save();
    assert!(obj.slug.len() <= 17);
}