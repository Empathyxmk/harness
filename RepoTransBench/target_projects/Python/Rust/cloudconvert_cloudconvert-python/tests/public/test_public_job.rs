use cloudconvert_cloudconvert_rust::job::Job;

#[test]
fn test_public_job_add_task() {
    let mut job = Job::new();
    job.add_task("task1".to_string());
    assert_eq!(job.tasks.len(), 1);
    assert_eq!(job.tasks[0], "task1");
}