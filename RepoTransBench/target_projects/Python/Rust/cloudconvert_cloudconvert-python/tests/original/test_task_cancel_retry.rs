use cloudconvert_cloudconvert_rust::task::{Task, TaskStatus};

#[test]
fn test_task_cancel() {
    let mut task = Task::new("import/url".to_string());
    task.status = TaskStatus::Processing;
    assert_eq!(task.cancel().unwrap(), ());
    assert_eq!(task.status, TaskStatus::Cancelled);
}

#[test]
fn test_retry_cancelled_task() {
    let mut task = Task::new("import/url".to_string());
    task.status = TaskStatus::Cancelled;
    let err = task.retry().unwrap_err();
    assert!(format!("{:?}", err).contains("Cannot retry a cancelled task"));
}