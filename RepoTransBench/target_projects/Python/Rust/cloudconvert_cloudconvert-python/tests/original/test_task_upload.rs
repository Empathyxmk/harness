use cloudconvert_cloudconvert_rust::task::{Task, TaskStatus};

#[test]
fn test_task_upload_success() {
    let mut task = Task::new("import/upload".to_string());
    let result = task.upload("file data".as_bytes());
    assert!(result.is_ok());
    assert_eq!(task.status, TaskStatus::Finished);
}

#[test]
fn test_task_upload_invalid() {
    let mut task = Task::new("import/upload".to_string());
    let result = task.upload(&[]);
    assert!(result.is_err());
}