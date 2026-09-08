use crate::errors::*;

#[test]
fn test_invalid_ciphertext_error() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", InvalidCiphertextError("Cipher error".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_invalid_range_limits_error() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", InvalidRangeLimitsError("Range error".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_out_of_range_error() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", OutOfRangeError("Out of range".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_not_enough_coins_error() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", NotEnoughCoinsError("No coins left".to_string()));
    });
    assert!(res.is_err());
}

#[test]
fn test_invalid_coin_error() {
    let res = std::panic::catch_unwind(|| {
        panic!("{}", InvalidCoinError("Invalid coin".to_string()));
    });
    assert!(res.is_err());
}