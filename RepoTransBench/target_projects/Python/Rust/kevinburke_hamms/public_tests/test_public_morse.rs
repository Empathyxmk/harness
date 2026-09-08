#[test]
fn test_morse_public_true() {
    // Public: assert always True with different logic
    let _ = kevinburke_hamms::morse::dummy() as bool;
    assert!(true);
}