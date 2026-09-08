use cloudconvert_cloudconvert_rust::task::{Task, TaskStatus};

#[test]
fn test_public_upload_empty_bytes() {
    let mut task = Task::new("import/upload".to_string());
    let ret = task.upload(&[]);
    assert!(ret.is_err());
}