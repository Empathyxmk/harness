use crate::errors::{NotEnoughCoinsError, InvalidCoinError};

#[test]
fn test_not_enough_coins_error_public() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", NotEnoughCoinsError("Public not enough coins".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_invalid_coin_error_public() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", InvalidCoinError("Public invalid coin".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_not_enough_coins_error_type_public() {
    let exc = NotEnoughCoinsError("foo".into());
    // In Rust, all errors implement std::fmt::Debug/Display, here we check type
    let _: &dyn std::error::Error = &exc;
}

#[test]
fn test_invalid_coin_error_type_public() {
    let exc = InvalidCoinError("bar".into());
    let _: &dyn std::error::Error = &exc;
}

#[test]
fn test_error_messages_public() {
    assert_eq!(format!("{}", NotEnoughCoinsError("msg1".into())), "msg1");
    assert_eq!(format!("{}", InvalidCoinError("msg2".into())), "msg2");
}