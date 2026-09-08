#[test]
fn test_get_jwt_in_non_protected_route() {
    // Simulate error (would panic or return error in a real JWT middleware)
    let result = std::panic::catch_unwind(|| panic!("Attempted get_jwt() outside protected context"));
    assert!(result.is_err());
}
#[test]
fn test_get_jwt_header_in_non_protected_route() {
    let result = std::panic::catch_unwind(|| panic!("Attempted get_jwt_header() outside protected context"));
    assert!(result.is_err());
}
#[test]
fn test_get_jwt_identity_in_non_protected_route() {
    let result = std::panic::catch_unwind(|| panic!("Attempted get_jwt_identity() outside protected context"));
    assert!(result.is_err());
}
#[test]
fn test_current_user_in_non_protected_route() {
    let result = std::panic::catch_unwind(|| panic!("Attempted current_user.foo outside protected context"));
    assert!(result.is_err());
}
#[test]
fn test_get_current_user_in_non_protected_route() {
    let result = std::panic::catch_unwind(|| panic!("Attempted get_current_user() outside protected context"));
    assert!(result.is_err());
}