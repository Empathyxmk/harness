use nickjj_ansible_docker::host_mock::{HostMock, VarValue};

use std::collections::HashMap;

#[test]
fn test_alternate_hostname() {
    let h = HostMock::new(
        Some("custom-server"),
        Some("ubuntu"),
        Some("debian"),
        None,
        None,
    );
    assert_eq!(h.hostname, "custom-server");
    assert_eq!(h.vars["inventory_hostname"], VarValue::String("custom-server".to_string()));
}

#[test]
fn test_different_os_family() {
    let h = HostMock::new(
        Some("web01"),
        Some("fedora"),
        Some("redhat"),
        None,
        None,
    );
    assert_eq!(h.os, "fedora");
    assert_eq!(h.family, "redhat");
    assert_eq!(h.vars["ansible_os_family"], VarValue::String("redhat".to_string()));
}

#[test]
fn test_groups_and_vars_public() {
    let mut vars = HashMap::new();
    vars.insert("extra".to_string(), VarValue::Int(123));
    let h = HostMock::new(
        None,
        None,
        None,
        Some(vec!["docker", "backend"]),
        Some(vars.clone()),
    );
    assert_eq!(h.groups, vec!["docker".to_string(), "backend".to_string()]);
    assert_eq!(h.vars["extra"], VarValue::Int(123));
    assert_eq!(h.vars["docker_host"], VarValue::String("unix:///var/run/docker.sock".to_string()));
}

#[test]
fn test_getitem_public() {
    let mut vars = HashMap::new();
    vars.insert("x".to_string(), VarValue::Int(100));
    let h = HostMock::new(None, None, None, None, Some(vars.clone()));
    assert_eq!(h["x"], VarValue::Int(100));
}

#[test]
fn test_vars_merging_public() {
    let mut vars = HashMap::new();
    vars.insert("a".to_string(), VarValue::Int(90));
    vars.insert("docker_host".to_string(), VarValue::String("/tmp".to_string()));
    let h = HostMock::new(Some("merge"), None, None, None, Some(vars.clone()));
    // The vars provided at init should override builtins
    assert_eq!(h.vars["a"], VarValue::Int(90));
    assert_eq!(h.vars["docker_host"], VarValue::String("/tmp".to_string()));
    // Should still have core expected vars present
    assert!(h.vars.contains_key("inventory_hostname"));
}

#[test]
fn test_envvar_public() {
    let mut vars = HashMap::new();
    vars.insert("env".to_string(), VarValue::String("prod".to_string()));
    let h = HostMock::new(None, None, None, None, Some(vars.clone()));
    // Should just store extra var 'env'
    assert_eq!(h.vars["env"], VarValue::String("prod".to_string()));
}

#[test]
fn test_repr_output_public() {
    let h = HostMock::new(
        Some("visual"),
        Some("redhat"),
        Some("rhel"),
        None,
        None,
    );
    let rep = format!("{:?}", h);
    assert!(rep.contains("visual"));
    assert!(rep.contains("redhat"));
    assert!(rep.contains("rhel"));
}