use gurugio::error_printer;
use gurugio::error_return;

#[test]
fn test_error_printer() {
    // coverage: normal use
    assert_eq!(error_printer(Some("hello world")), 0);
    // coverage: NULL (error branch)
    assert_eq!(error_printer(None), -1);
}

#[test]
fn test_error_return() {
    // coverage: normal (error code)
    assert_eq!(error_return(5), 5);
    // coverage: no print branch
    assert_eq!(error_return(0), 0);
}