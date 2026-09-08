use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn api_public_thread_func(sum: Arc<Mutex<i32>>) -> i32 {
    thread::sleep(Duration::from_millis(9));
    let mut sum = sum.lock().unwrap();
    *sum += 5;
    42
}

#[test]
fn test_api_public_thread_func() {
    let res = Arc::new(Mutex::new(33));
    let res_clone = res.clone();
    let handle = thread::spawn(move || api_public_thread_func(res_clone));
    let retval = handle.join().unwrap();
    assert_eq!(*res.lock().unwrap(), 38);
    assert_eq!(retval, 42);

    thread::yield_now();

    let id = thread::current().id();
    assert!(format!("{:?}", id).len() > 0);
}