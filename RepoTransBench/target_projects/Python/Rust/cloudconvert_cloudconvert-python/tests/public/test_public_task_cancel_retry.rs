use cloudconvert_cloudconvert_rust::task::{Task, TaskStatus};

#[test]
fn test_public_task_cancel_pending() {
    let mut task = Task::new("dummy".to_string());
    assert!(task.cancel().is_ok());
    assert_eq!(task.status, TaskStatus::Cancelled);
}