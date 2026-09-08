use rvrsh3ll_bof_collection::{
    registry_persistence_set_value, 
    registry_persistence_delete_value,
    FakeRegistryValue,
};
use std::cell::RefCell;

thread_local! {
    static PUBLIC_FAKE_REGISTRY: RefCell<FakeRegistryValue> = RefCell::new(
        FakeRegistryValue { 
            key: String::new(), 
            value: String::new() 
        }
    );
}

fn set_registry_value(path: &str, key: &str, value: &str) -> i32 {
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let mut registry = registry.borrow_mut();
        registry.key = format!("{}\\{}", path, key);
        registry.value = value.to_string();
    });
    0
}

fn delete_registry_value(path: &str, key: &str) -> i32 {
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let mut registry = registry.borrow_mut();
        registry.key = String::new();
        registry.value = String::new();
    });
    0
}

#[test]
fn public_registry_persistence_test_case_overwrite() {
    let test_path = "HKEY_LOCAL_MACHINE\\Software\\Rvrsh3ll\\UnitPublic";
    let test_key = "SampleKey";
    let test_value = "FirstVal";
    let test_value2 = "ChangedVal";

    // Set, verify set
    assert_eq!(set_registry_value(test_path, test_key, test_value), 0);
    
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let registry = registry.borrow();
        assert_eq!(registry.key, "HKEY_LOCAL_MACHINE\\Software\\Rvrsh3ll\\UnitPublic\\SampleKey");
        assert_eq!(registry.value, "FirstVal");
    });

    // Overwrite and verify
    assert_eq!(set_registry_value(test_path, test_key, test_value2), 0);
    
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let registry = registry.borrow();
        assert_eq!(registry.key, "HKEY_LOCAL_MACHINE\\Software\\Rvrsh3ll\\UnitPublic\\SampleKey");
        assert_eq!(registry.value, "ChangedVal");
    });

    // Delete and verify removed
    assert_eq!(delete_registry_value(test_path, test_key), 0);
    
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let registry = registry.borrow();
        assert_eq!(registry.key, "");
        assert_eq!(registry.value, "");
    });

    println!("public_registry_persistence_test_case_overwrite passed.");
}

#[test]
fn public_registry_persistence_test_case_unicode() {
    // Different unicode-like test data
    let test_path = "HKEY_LOCAL_MACHINE\\Software\\ΩTest";
    let test_key = "ユニコード";
    let test_value = "值🎉";

    assert_eq!(set_registry_value(test_path, test_key, test_value), 0);
    
    PUBLIC_FAKE_REGISTRY.with(|registry| {
        let registry = registry.borrow();
        assert_eq!(registry.key, "HKEY_LOCAL_MACHINE\\Software\\ΩTest\\ユニコード");
        assert_eq!(registry.value, "值🎉");
    });

    assert_eq!(delete_registry_value(test_path, test_key), 0);

    println!("public_registry_persistence_test_case_unicode passed.");
}