use wjcryptlib::aesofboutput;

#[test]
fn test_no_arguments() {
    let result = aesofboutput::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_short_key() {
    let args = ["123", "0001020304050607", "16"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_err());
}

#[test]
fn test_short_iv() {
    let args = ["000102030405060708090a0b0c0d0e0f", "00000000000", "16"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_err());
}

#[test]
fn test_invalid_numbytes() {
    let args = ["000102030405060708090a0b0c0d0e0f", "0001020304050607", "notanumber"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_err());
}

#[test]
fn test_valid_call() {
    let args = ["000102030405060708090a0b0c0d0e0f", "0001020304050607", "16"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_ok());
}