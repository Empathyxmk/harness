use wjcryptlib::aesblock;
use hex::FromHex;

#[test]
fn test_no_arguments() {
    // In C: Calls the binary with no arguments and expects error/usage.
    // In Rust: simulate call with empty args
    let result = aesblock::run_command(&[]);
    assert!(result.is_err(), "Expected error due to no arguments");
}

#[test]
fn test_short_key_length() {
    let args = [
        "123",
        "1234567890abcdef0123456789abcdef",
        "0001020304050607",
        "0001020304050607",
        "16",
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Short key should produce error");
}

#[test]
fn test_short_iv_length() {
    let args = [
        "000102030405060708090a0b0c0d0e0f",
        "1234567890abcdef0123456789abcdef",
        "00010203040506",
        "0001020304050607",
        "16",
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Short IV should produce error");
}

#[test]
fn test_short_inputblock_length() {
    let args = [
        "000102030405060708090a0b0c0d0e0f",
        "1234567890abcdef0123456789abcdef",
        "0001020304050607",
        "00010203040506",
        "16",
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Short input should produce error");
}

#[test]
fn test_short_numbytes() {
    let args = [
        "000102030405060708090a0b0c0d0e0f",
        "1234567890abcdef0123456789abcdef",
        "0001020304050607",
        "0001020304050607",
        "wrong"
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Non-numeric numbytes should error");
}

#[test]
fn test_full_valid_call() {
    let args = [
        "000102030405060708090a0b0c0d0e0f",
        "000102030405060708090a0b0c0d0e0f",
        "0001020304050607",
        "0001020304050607",
        "16"
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_ok(), "Valid call should succeed");
}