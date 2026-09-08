use vijos_jd4::pool::{put_sandbox, get_sandbox, init};

#[test]
fn test_public_put_sandbox_puts_to_queue() {
    {
        let mut guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        guard.clear();
    }
    put_sandbox(10, 11, 12);
    let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
    let vals: Vec<_> = guard.iter().cloned().collect();
    assert_eq!(vals, vec![10, 11, 12]);
}

#[tokio::test]
async fn test_public_get_sandbox() {
    {
        let mut guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        guard.clear();
        guard.push_back(21);
        guard.push_back(22);
    }
    let outs = get_sandbox(2).await;
    assert_eq!(outs, vec![21, 22]);
}

#[test]
fn test_public_init_parallelism() {
    init();
    {
        let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        assert!(guard.len() > 0);
    }
}

#[test]
fn test_public_init_low_parallelism() {
    init();
    {
        let guard = vijos_jd4::pool::SANDBOXES.lock().unwrap();
        assert!(guard.len() > 0);
    }
}