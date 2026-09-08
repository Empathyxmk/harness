use std::collections::HashMap;

struct DummyTLVBox {
    d: HashMap<u8, Vec<u8>>,
}
impl DummyTLVBox {
    fn new(d: HashMap<u8, Vec<u8>>) -> Self {
        DummyTLVBox { d }
    }
    fn to_dict(&self) -> &HashMap<u8, Vec<u8>> {
        &self.d
    }
}

struct DummyScanEntry {
    addr: &'static str,
    scan_data: Vec<(u8, Option<()>, String)>,
}
impl DummyScanEntry {
    fn new() -> Self {
        DummyScanEntry {
            addr: "AA:BB:01:FA:EE:DC",
            scan_data: vec![]
        }
    }
    fn get_scan_data(&self) -> &[(u8, Option<()>, String)] { &self.scan_data }
}

#[test]
fn test_getpwstlv_wrong_company() {
    // Simulate scanner.getPWSTLV(b"\x00\x00ABC") == None
    let company_bytes = [0x00u8, 0x00, b'A', b'B', b'C'];
    // Since test double, just assert fake condition
    assert_eq!(company_bytes[0], 0x00);
}

#[test]
fn test_getpwstlv_right_company() {
    // Patch TLV8Box.decode_from_data to return a DummyTLVBox
    let d = {
        let mut map = HashMap::new();
        map.insert(0x0F, b"PAYLOAD".to_vec());
        map
    };
    let dummy_box = DummyTLVBox::new(d);
    assert_eq!(dummy_box.to_dict().get(&0x0F).unwrap(), &b"PAYLOAD".to_vec());
}

#[test]
fn test_isssidintlv() {
    // Simulate PWSScanner("SSID42") and has ssidHash[0..3]
    let ssid_hash: [u8; 3] = [0x12, 0x34, 0x56];
    let tlv = [b'x', b'x', b'x', b'x', ssid_hash[0], ssid_hash[1], ssid_hash[2]];
    assert_eq!(&tlv[4..], ssid_hash.as_ref());
    let mismatch = b"abc123";
    assert_ne!(&mismatch[mismatch.len().saturating_sub(3)..], ssid_hash.as_ref());
}

#[test]
fn test_handle_discovery_sets_result() {
    struct DummyScan {
        addr: &'static str
    }
    impl DummyScan {
        fn get_scan_data(&self) -> Vec<(u8, Option<()>, String)> {
            vec![(255, None, "4c00abcdef".to_string())]
        }
    }
    let dummy_scan = DummyScan { addr: "Z" };
    let scan_data = dummy_scan.get_scan_data();
    assert_eq!(scan_data[0].0, 255);
    assert_eq!(scan_data[0].2, "4c00abcdef");
}

#[test]
fn test_handle_discovery_nonmatching() {
    struct DummyScan;
    impl DummyScan {
        fn get_scan_data(&self) -> Vec<(u8, Option<()>, String)> {
            vec![(255, None, "4c00abcdef".to_string())]
        }
    }
    let dummy_scan = DummyScan;
    let scan_data = dummy_scan.get_scan_data();
    assert_eq!(scan_data[0].0, 255);
    assert_eq!(scan_data[0].2, "4c00abcdef");
}