// Translation of tests/test_settings.py

use mattupstate_overholt::settings;

#[test]
fn test_settings_values() {
    assert_eq!(settings::DEBUG, true);
    assert_eq!(settings::SECRET_KEY, "super-secret-key");
    assert_eq!(settings::SECURITY_SEND_REGISTER_EMAIL, false);
}