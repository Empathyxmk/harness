use crate::manager::Manager;

#[test]
fn test_public_manager_add_and_get() {
    let mut mgr = Manager::new();
    mgr.add_process("new-proc", "echo testpublic");
    let procs = &mgr.processes;
    assert!(procs.contains_key("new-proc"));
    assert_eq!(procs["new-proc"].command, "echo testpublic");
}

#[test]
fn test_public_manager_ensure_unique_name() {
    let mut mgr = Manager::new();
    mgr.add_process("foo", "cmd1");
    let res = std::panic::catch_unwind(|| {
        mgr.add_process("foo", "cmd2");
    });
    assert!(res.is_err());
}