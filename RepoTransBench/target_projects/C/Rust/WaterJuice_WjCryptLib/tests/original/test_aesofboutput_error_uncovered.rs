use wjcryptlib::aesofboutput;

#[test]
fn test_invalid_key_length() {
    let args = ["01020304", "1234567890abcdef", "16"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_err(), "Too short key must fail");
}

#[test]
fn test_invalid_iv_length() {
    let args = ["00112233445566778899aabbccddeeff", "01020304", "8"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_err(), "Too short IV must fail");
}

#[test]
fn test_length_not_multiple_of_16() {
    let args = ["00112233445566778899aabbccddeeff", "1234567890abcdef", "17"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_ok(), "Should not error on 17 length");
}

#[test]
fn test_correct_call_produce_odd_output() {
    let args = ["00112233445566778899aabbccddeeff", "1234567890abcdef", "32"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_ok());
}

#[test]
fn test_length_zero() {
    let args = ["00112233445566778899aabbccddeeff", "1234567890abcdef", "0"];
    let result = aesofboutput::run_command(&args);
    assert!(result.is_ok());
}