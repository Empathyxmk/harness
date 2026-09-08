// Translated from tests/parse_prefix_public_test.c

fn parse_prefix(input: Option<&str>, output: &mut [u8]) -> i32 {
    match input {
        None => return -1,
        Some(s) => {
            if output.len() == 0 {
                return -1;
            }
            let bytes = s.as_bytes();
            if bytes.len() + 1 > output.len() {
                return -2;
            }
            output[..bytes.len()].copy_from_slice(bytes);
            // Null terminate
            if bytes.len() < output.len() {
                output[bytes.len()] = 0;
            }
            0
        }
    }
}

#[test]
fn test_parse_prefix_basic_public() {
    let mut output = [0u8; 20];
    let ret = parse_prefix(Some("xyz123"), &mut output);
    assert_eq!(ret, 0);
    let result = std::ffi::CStr::from_bytes_until_nul(&output).unwrap();
    assert_eq!(result.to_str().unwrap(), "xyz123");
}

#[test]
fn test_parse_prefix_null_input_public() {
    let mut output = [0u8; 8];
    let ret = parse_prefix(None, &mut output);
    assert_eq!(ret, -1);
}

#[test]
fn test_parse_prefix_null_output_public() {
    let ret = parse_prefix(Some("test"), &mut []);
    assert_eq!(ret, -1);
}

#[test]
fn test_parse_prefix_overflow_public() {
    let mut output = [0u8; 4];
    let ret = parse_prefix(Some("overflow"), &mut output);
    assert_eq!(ret, -2);
}