// Public tests for helpers: shout and invert_bool

use samplemod_rs::helpers;

#[test]
fn test_shout_public() {
    assert_eq!(helpers::shout("public"), "PUBLIC!");
}

#[test]
fn test_invert_bool_public_true() {
    assert_eq!(helpers::invert_bool(true), false);
}

#[test]
fn test_invert_bool_public_false() {
    assert_eq!(helpers::invert_bool(false), true);
}

#[test]
fn test_shout_public_numbers() {
    assert_eq!(helpers::shout("123"), "123!");
}