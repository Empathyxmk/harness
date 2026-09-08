use openwifipass::keys::*;

#[test]
fn test_key_constants() {
    assert_eq!(BLE_MFG_ID, 0x004C);
    assert_eq!(PWS_TYPE, 0x0F);
}

#[test]
fn test_get_ble_vendor() {
    assert_eq!(get_ble_vendor(), 0x004C);
}

#[test]
fn test_get_pws_type() {
    assert_eq!(get_pws_type(), 0x0F);
}

#[test]
fn test_session_keys() {
    let sk = SessionKeys::new();
    assert_eq!(sk.get(), "dummy_session_key");
}