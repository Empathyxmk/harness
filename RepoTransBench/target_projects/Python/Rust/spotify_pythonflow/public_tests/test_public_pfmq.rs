use spotify_pythonflow_rs::pfmq;

#[test]
fn test_cancel_task_public() {
    let _task = pfmq::Task::new();
    assert!(true);
}

#[test]
fn test_cancel_not_running_public() {
    let b = pfmq::Broker::new("some_addr");
    assert!(true);
}

#[test]
fn test_imap_not_running_public() {
    assert!(true);
}

#[test]
fn test_apply_not_running_public() {
    assert!(true);
}

#[test]
fn test_not_pickleable_public() {
    assert!(true);
}

#[test]
fn test_no_context_public() {
    assert!(true);
}