use bdarnell_plop::platform;

#[test]
fn test_get_hostname() {
    let h = platform::get_hostname();
    assert!(!h.is_empty());
}

#[test]
fn test_get_username() {
    let u = platform::get_username();
    assert!(!u.is_empty());
}