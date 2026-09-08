use gurugio::error_printer;
use gurugio::error_return;

#[test]
fn test_error_printer_public() {
    // Different messages from original test
    assert_eq!(error_printer(Some("public message example")), 0);
    // Still test NULL, required branch
    assert_eq!(error_printer(None), -1);
}

#[test]
fn test_error_return_public() {
    // Different error codes
    assert_eq!(error_return(10), 10);
    assert_eq!(error_return(-7), -7);
    // Still test zero, required branch
    assert_eq!(error_return(0), 0);
}