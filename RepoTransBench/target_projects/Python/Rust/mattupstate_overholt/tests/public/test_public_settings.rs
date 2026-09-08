// Translation of public_tests/test_public_settings.py

use mattupstate_overholt::settings;

#[test]
fn test_settings_public_values() {
    let secret = settings::SECRET_KEY;
    assert!(secret.len() >= 8);
    assert!(!secret.is_empty());
    assert!(matches!(settings::DEBUG, true | false));
    assert!(matches!(settings::SECURITY_SEND_REGISTER_EMAIL, true | false));
}