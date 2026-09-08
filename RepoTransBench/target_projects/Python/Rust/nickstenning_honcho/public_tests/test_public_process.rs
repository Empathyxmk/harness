use crate::process::Process;
use std::collections::HashMap;

#[test]
fn test_public_process_init() {
    let mut env = HashMap::new();
    env.insert("HELLO".to_string(), "world".to_string());
    let p = Process::new("worker.3", "proc_cmd", Some(env.clone()));
    assert_eq!(p.name, "worker.3");
    assert_eq!(p.cmd, "proc_cmd");
    assert_eq!(p.env.get("HELLO").unwrap(), "world");
}