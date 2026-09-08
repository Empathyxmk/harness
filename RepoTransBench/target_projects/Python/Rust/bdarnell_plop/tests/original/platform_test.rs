use bdarnell_plop::platform;

#[test]
fn test_setitimer_available() {
    // We simulate setitimer always available for this Rust port
    assert!(platform::setitimer());
}

#[test]
fn test_itimer_constants() {
    assert_eq!(platform::ITIMER_REAL, 0);
    assert_eq!(platform::ITIMER_VIRTUAL, 1);
    assert_eq!(platform::ITIMER_PROF, 2);
}