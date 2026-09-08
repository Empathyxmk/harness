use cloudconvert_cloudconvert_rust::job::{Job, JobStatus};

#[test]
fn test_job_new_defaults() {
    let job = Job::new();
    assert_eq!(job.status, JobStatus::Pending);
    assert_eq!(job.tasks.len(), 0);
}

#[test]
fn test_job_add_task() {
    let mut job = Job::new();
    job.add_task("import-file".to_string());
    assert_eq!(job.tasks.len(), 1);
    assert_eq!(job.tasks[0], "import-file");
}