use cloudconvert_cloudconvert_rust::error::{CloudConvertError, ErrorKind};

#[test]
fn test_error_kind_api() {
    let err = CloudConvertError::api("API error!");
    match err.kind {
        ErrorKind::API(ref message) => assert_eq!(message, "API error!"),
        _ => panic!("unexpected error kind"),
    }
}

#[test]
fn test_error_kind_network() {
    let err = CloudConvertError::network("Network error!");
    match err.kind {
        ErrorKind::Network(ref message) => assert_eq!(message, "Network error!"),
        _ => panic!("unexpected error kind"),
    }
}

#[test]
fn test_error_kind_invalid_data() {
    let err = CloudConvertError::invalid_data("Invalid!");
    match err.kind {
        ErrorKind::InvalidData(ref message) => assert_eq!(message, "Invalid!"),
        _ => panic!("unexpected error kind"),
    }
}