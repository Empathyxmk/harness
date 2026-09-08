use pywizlight_rust::discovery::{wiz_mdns_name, default_mac};

#[test]
fn test_wiz_mdns_name_public() {
    // Use new MAC format
    let mac = "11:22:33:44:55:66";
    assert_eq!(wiz_mdns_name(mac), "WIZ_112233445566._wiz._udp.local.");
}

#[test]
fn test_default_mac_public() {
    let ip = "192.168.2.22";
    let port = 9020;
    let mac = default_mac(ip, port);
    assert_eq!(mac, "C0A80216232C");
}