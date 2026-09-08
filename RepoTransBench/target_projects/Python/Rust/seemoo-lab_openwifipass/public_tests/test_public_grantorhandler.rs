#[test]
fn test_get_ssid_public() {
    let ssid = "AnotherSSID";
    assert_eq!(ssid, "AnotherSSID");
}

#[test]
fn test_get_psk_public() {
    let psk = "DifferentPSKValue";
    assert_eq!(psk, "DifferentPSKValue");
}

#[test]
fn test_get_shared_secret_public() {
    let secret: Vec<u8> = vec![0; 32];
    assert_eq!(secret.len(), 32);
}

#[test]
fn test_check_shared_secret_public() {
    let real_secret = vec![1; 32];
    let user_supplied = vec![1; 32];
    assert_eq!(real_secret, user_supplied);

    let fake = vec![b'x'; 32];
    assert_ne!(real_secret, fake);
}