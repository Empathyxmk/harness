// Original test_cron.py - Simulated as REST API calls in Python FastAPI; Here mocked as function calls.

#[derive(Default)]
struct MockJobScheduler {
    jobs: Vec<String>,
}

impl MockJobScheduler {
    fn new() -> Self {
        Self { jobs: vec![] }
    }
    fn add_job(&mut self, job_id: &str) -> (&'static str, usize) {
        self.jobs.push(job_id.to_string());
        ("added", 200)
    }

    fn get_all_jobs(&self) -> (&'static str, usize, usize) {
        ("ok", 200, self.jobs.len())
    }

    fn del_job(&mut self, job_id: &str) -> (&'static str, usize) {
        self.jobs.retain(|jid| jid != job_id);
        ("deleted", 200)
    }
}

#[test]
fn test_add_job() {
    let mut scheduler = MockJobScheduler::new();
    let (msg, code) = scheduler.add_job("123");
    assert_eq!(msg, "added");
    assert_eq!(code, 200);
    assert!(scheduler.jobs.contains(&"123".to_string()));
}

#[test]
fn test_get_all_job() {
    let mut scheduler = MockJobScheduler::new();
    scheduler.add_job("123");
    let (msg, code, count) = scheduler.get_all_jobs();
    assert_eq!(msg, "ok");
    assert_eq!(code, 200);
    assert!(count >= 1);
}

#[test]
fn test_del_job() {
    let mut scheduler = MockJobScheduler::new();
    scheduler.add_job("123");
    let (msg, code) = scheduler.del_job("123");
    assert_eq!(msg, "deleted");
    assert_eq!(code, 200);
    assert!(!scheduler.jobs.contains(&"123".to_string()));
}