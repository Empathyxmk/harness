use cloudconvert_cloudconvert_rust::error::{CloudConvertError, ErrorKind};

#[test]
fn test_public_cloudconvert_api_error() {
    let err = CloudConvertError::api("boom");
    match err.kind {
        ErrorKind::API(ref msg) => assert_eq!(msg, "boom"),
        _ => panic!("Wrong error type!"),
    }
}