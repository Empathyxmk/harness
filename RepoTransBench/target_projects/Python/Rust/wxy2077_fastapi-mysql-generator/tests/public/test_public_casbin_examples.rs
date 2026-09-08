use casbin::{prelude::*, Adapter, Result as CasbinResult, Enforcer};
use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

fn dir_path() -> String {
    "public_tests/demo_casbin".to_string()
}

#[test]
fn test_01_demo_enforcement_public() {
    let model_path = format!("{}/model.conf", dir_path());
    let policy_path = format!("{}/policy.csv", dir_path());
    let mut e = Enforcer::new(model_path, policy_path).unwrap();
    // Different subjects/resources/actions compared to private tests
    assert!(!e.enforce(&["alice2", "data2", "write"]).unwrap());
    assert!(e.enforce(&["alice2", "data2", "read"]).unwrap());
    assert!(!e.enforce(&["bob2", "data2", "read"]).unwrap());
    assert!(e.enforce(&["bob2", "data2", "write"]).unwrap());
    assert!(!e.enforce(&["bob2", "data1", "read"]).unwrap());
    assert!(e.enforce(&["root2", "data1", "delete"]).unwrap());
    assert!(!e.enforce(&["root2", "data1", "update"]).unwrap());
}

#[test]
fn test_02_orm_adapter_public() {
    let model_path = format!("{}/model.conf", dir_path());
    let policy_path = format!("{}/policy.csv", dir_path());
    // FileAdapter
    let mut e = Enforcer::new(model_path, policy_path).unwrap();
    assert!(e.enforce(&["alice2", "data2", "read"]).unwrap());
    assert!(!e.enforce(&["alice2", "data2", "write"]).unwrap());
}

#[test]
fn test_03_custom_orm_public() {
    let model_path = format!("{}/custom_model.conf", dir_path());
    // Hardcode a temporary csv for this test
    let tmpdir = std::env::temp_dir();
    let custom_policy = tmpdir.join("custom_policy.csv");
    let mut file = File::create(&custom_policy).unwrap();
    writeln!(file, "p, john, domain_public, data9, access").unwrap();
    writeln!(file, "p, jane, domain_public, data9, read").unwrap();
    writeln!(file, "p, john, domain_public, data10, modify").unwrap();
    let mut e = Enforcer::new(model_path, custom_policy.to_str().unwrap()).unwrap();
    assert!(e.enforce(&["john", "domain_public", "data9", "access"]).unwrap());
    assert!(!e.enforce(&["john", "domain_public", "data9", "read"]).unwrap());
    assert!(e.enforce(&["john", "domain_public", "data10", "modify"]).unwrap());
    assert!(!e.enforce(&["jane", "domain_public", "data9", "access"]).unwrap());
    assert!(e.enforce(&["jane", "domain_public", "data9", "read"]).unwrap());
}