use std::collections::HashMap;
use std::cell::RefCell;

thread_local! {
    static FAKECLI_CALLED: RefCell<bool> = RefCell::new(false);
}

struct NoVaultSecretFoundPublic;

#[test]
fn test_no_vault_secret_found_public() {
    let ex = NoVaultSecretFoundPublic;
    let _: &NoVaultSecretFoundPublic = &ex;
}

struct FakeCLIPublic;
impl FakeCLIPublic {
    fn setup_vault_secrets(
        _loader: &str,
        _vault_ids: &Vec<String>,
        _vault_password_files: &Vec<String>,
        _ask_vault_pass: bool,
    ) {
        FAKECLI_CALLED.with(|f| *f.borrow_mut() = true);
    }
}

struct DummyLoaderPublic;
struct DummyIMPublic {
    _sources: Vec<String>,
    _loader: DummyLoaderPublic,
}
impl DummyIMPublic {
    fn new() -> Self {
        DummyIMPublic {
            _sources: vec!["/var/xyz".to_string()],
            _loader: DummyLoaderPublic,
        }
    }
    fn groups(&self) -> HashMap<String, String> {
        HashMap::new()
    }
}

struct DummyGroupPublic;
struct DummyPluginPublic {
    called: RefCell<bool>,
}
impl DummyPluginPublic {
    fn new() -> Self {
        DummyPluginPublic { called: RefCell::new(false) }
    }
    fn get_vars(&self, _loader: &DummyLoaderPublic, _path: &str, _entities: &Vec<DummyGroupPublic>) -> HashMap<String, String> {
        *self.called.borrow_mut() = true;
        [("baz".to_string(), "qux".to_string())].iter().cloned().collect()
    }
}

struct DummyPluginHostPublic;
impl DummyPluginHostPublic {
    fn get_host_vars(&self, _name: &str) -> HashMap<String, i32> { [("a".to_string(), 82)].iter().cloned().collect() }
    fn get_group_vars(&self, _name: &str) -> HashMap<String, i32> { [("b".to_string(), 99)].iter().cloned().collect() }
}

struct DummyHostPublic {
    name: String,
}
impl DummyHostPublic {
    fn new(name: &str) -> Self { DummyHostPublic { name: name.to_string() } }
}

#[test]
fn test_ansibleinventory_public_init() {
    FAKECLI_CALLED.with(|f| *f.borrow_mut() = false);
    FakeCLIPublic::setup_vault_secrets("", &vec![], &vec![], false);
    assert_eq!(FAKECLI_CALLED.with(|f| *f.borrow()), true);
}

#[test]
fn test_plugins_inventory_public() {
    let dummy_im = DummyIMPublic::new();
    let plugin = DummyPluginPublic::new();
    let result = plugin.get_vars(&dummy_im._loader, "/", &vec![]);
    assert_eq!(result.get("baz"), Some(&"qux".to_string()));
}

#[test]
fn test_get_plugin_vars_host_public() {
    let plugin = DummyPluginHostPublic;
    let out = plugin.get_host_vars("test_name");
    assert_eq!(out.get("a"), Some(&82));
}

#[test]
fn test_get_group_vars_public() {
    fn plugins_inventory(_e: Vec<DummyGroupPublic>) -> HashMap<String, String> {
        [("other".to_string(), "groupvar2".to_string())].iter().cloned().collect()
    }
    let result = plugins_inventory(vec![]);
    assert_eq!(result.get("other"), Some(&"groupvar2".to_string()));
}

#[test]
fn test_get_host_vars_magic_public() {
    struct DummyVM2;
    impl DummyVM2 {
        fn get_vars(&self, _host: &str, _include_hostvars: bool) -> HashMap<&'static str, i32> {
            [("persist", 42), ("omit", 0), ("ansible_version", -1)].iter().cloned().collect()
        }
    }
    let vm = DummyVM2;
    let vars = vm.get_vars("hh", true);
    assert!(vars.contains_key("persist"));
    assert_eq!(vars.get("omit"), Some(&0));
    assert_eq!(vars.get("ansible_version"), Some(&-1));
}

#[test]
fn test_get_host_vars_ansible_error_public() {
    struct DummyVM3;
    impl DummyVM3 {
        fn get_vars(&self, _host: &str) -> Result<(), String> {
            Err("fail!".to_string())
        }
    }
    let vm = DummyVM3;
    let result = vm.get_vars("hh");
    assert!(result.is_err());
}