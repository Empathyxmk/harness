use vijos_jd4::pool::{put_sandbox, get_sandbox, init};

#[test]
fn test_put_sandbox_puts_to_queue() {
    // Reset sandbox queue to empty
    {
        let mut guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        guard.clear();
    }
    put_sandbox(1, 2, 3);
    let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
    let vals: Vec<_> = guard.iter().cloned().collect();
    assert_eq!(vals, vec![1, 2, 3]);
}

#[tokio::test]
async fn test_get_sandbox() {
    // Pre-populate SANDBOXES
    {
        let mut guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        guard.clear();
        guard.push_back(1);
        guard.push_back(2);
    }
    let out = get_sandbox(2).await;
    assert_eq!(out, vec![1, 2]);
}

#[test]
fn test_init_parallelism() {
    // Just call init and verify queue is populated
    init();
    {
        let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        assert!(guard.len() > 0);
    }
}

#[test]
fn test_init_low_parallelism() {
    // Call init, queue must still exist
    init();
    {
        let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        assert!(guard.len() > 0);
    }
}