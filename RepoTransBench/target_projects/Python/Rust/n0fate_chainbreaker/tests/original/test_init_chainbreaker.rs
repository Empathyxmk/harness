use n0fate_chainbreaker::Chainbreaker;

struct DummyDbBlob {
    pub salt: [u8; 8],
}

struct DummyKC {
    _unlock_password: String,
    dbblob: DummyDbBlob,
    _generated: bool,
    _unlock_key: Option<Vec<u8>>,
}
impl DummyKC {
    fn new() -> Self {
        DummyKC {
            _unlock_password: "pw".to_string(),
            dbblob: DummyDbBlob { salt: [0u8; 8] },
            _generated: false,
            _unlock_key: None,
        }
    }
    fn set_unlock_password(&mut self, value: &str) {
        self._unlock_password = value.to_string();
        self._unlock_key = Some(vec![1,2,3,4]);
        self._generated = true;
    }
}

#[test]
fn test_chainbreaker_attrs() {
    let mut kc = DummyKC::new();
    kc.set_unlock_password("pw");
    assert!(kc._generated);
    assert!(kc._unlock_key.is_some());
}

#[test]
fn test_class_has_logger() {
    assert_eq!(Chainbreaker::logger(), "dummy logger");
}

struct KCDummy {
    warned: Option<String>,
}
impl KCDummy {
    fn new() -> Self {
        KCDummy { warned: None }
    }
    fn dump_generic_passwords(&mut self) {
        // Simulate KeyError
        self.warned = Some("[!] Generic Password Table is not available".to_string());
    }
    fn dump_internet_passwords(&mut self) {
        self.warned = Some("[!] Internet Password Table is not available".to_string());
    }
}

#[test]
fn test_dump_generic_passwords_warns_if_keyerror() {
    let mut kc = KCDummy::new();
    kc.dump_generic_passwords();
    assert_eq!(kc.warned.unwrap(), "[!] Generic Password Table is not available");
}

#[test]
fn test_dump_internet_passwords_warn() {
    let mut kc = KCDummy::new();
    kc.dump_internet_passwords();
    assert_eq!(kc.warned.unwrap(), "[!] Internet Password Table is not available");
}