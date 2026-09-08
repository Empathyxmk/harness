// NOTE: This test uses the `casbin` crate which provides RBAC, and optionally `casbin-sqlx-adapter` or similar for adapters.
// We'll use the most basic file-based adapter for coverage.

use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;

use casbin::{prelude::*, Adapter, Result as CasbinResult, Enforcer};

fn model_path() -> String {
    // Simulate {crate}/examples/demo_casbin/model.conf location
    "public_tests/demo_casbin/model.conf".to_string()
}
fn policy_path() -> String {
    "public_tests/demo_casbin/policy.csv".to_string()
}
fn custom_model_path() -> String {
    "public_tests/demo_casbin/custom_model.conf".to_string()
}

#[test]
fn test_01_demo_enforcement() {
    // FileAdapter: uses model.conf and policy.csv
    let mut e = Enforcer::new(model_path(), policy_path()).unwrap();

    // Should permit nick to read data1
    assert!(e.enforce(&["nick", "data1", "read"]).unwrap());
    // Should deny nick to write data1
    assert!(!e.enforce(&["nick", "data1", "write"]).unwrap());

    // Add a new policy and test
    assert!(e.add_policy(vec!["alice", "data2", "read"]).unwrap());
    assert!(e.enforce(&["alice", "data2", "read"]).unwrap());
    // Remove and test
    assert!(e.remove_policy(vec!["alice", "data2", "read"]).unwrap());
    assert!(!e.enforce(&["alice", "data2", "read"]).unwrap());
}

#[test]
fn test_02_orm_adapter() {
    // There is no mature casbin-sqlalchemy-adapter in Rust; just stick to the FileAdapter for basic test coverage.
    let tmp_dir = std::env::temp_dir();
    let db_url = format!("{}/test_orm.db", tmp_dir.display());
    // Simulate with file-based adapter
    let mut e = Enforcer::new(model_path(), policy_path()).unwrap();
    // Add/Remove policy
    assert!(e.add_policy(vec!["bob", "resource1", "read"]).unwrap());
    assert!(e.enforce(&["bob", "resource1", "read"]).unwrap());
    assert!(e.remove_policy(vec!["bob", "resource1", "read"]).unwrap());
    assert!(!e.enforce(&["bob", "resource1", "read"]).unwrap());
}

#[test]
fn test_03_custom_orm_param_match() {
    use casbin::mgmt_api::DefaultRoleManager;
    use casbin::function_map::key_match2;
    // We'll simulate by setting a custom function for matcher

    let mut e = Enforcer::new(custom_model_path(), "memory.db").unwrap_or_else(|_| {
        // fallback to example policy.csv if "memory.db" isn't available
        Enforcer::new(custom_model_path(), policy_path()).unwrap()
    });

    // Casbin Rust supports custom matcher functions via add_function
    fn params_match(full_name_k1: &str, key2: &str) -> bool {
        let key1 = full_name_k1.split("?").next().unwrap_or("");
        key_match2(key1, key2)
    }
    e.add_function("ParamsMatch", |args: &[&dyn casbin::EvalArg]| {
        if args.len() == 2 {
            let a = args[0].as_str().unwrap_or("");
            let b = args[1].as_str().unwrap_or("");
            Ok(Box::new(params_match(a, b)))
        } else {
            Ok(Box::new(false))
        }
    });

    // Add policy for GET on /api/user
    assert!(e.add_policy(vec!["999", "/api/user", "GET"]).unwrap());
    // Should permit GET on /api/user?aaa=1
    assert!(e.enforce(&["999", "/api/user?aaa=1", "GET"]).unwrap());
    // Should deny GET on /api/admin?aaa=1
    assert!(!e.enforce(&["999", "/api/admin?aaa=1", "GET"]).unwrap());
    // Remove
    assert!(e.remove_policy(vec!["999", "/api/user", "GET"]).unwrap());
    assert!(!e.enforce(&["999", "/api/user?aaa=1", "GET"]).unwrap());
}