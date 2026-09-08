use std::sync::Mutex;
use std::thread;
use std::sync::Condvar;
use std::sync::Once;
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};

fn noop_func(_arg: Option<&mut i32>) -> i32 {
    0
}

#[test]
fn test_thread_start_stop() {
    let handle = thread::spawn(|| noop_func(None));
    handle.join().unwrap();
    println!("test_thread_start_stop: PASS");
}

#[test]
fn test_mutex_init_destroy_lock_unlock() {
    let m = Mutex::new(());
    {
        let _g = m.lock().unwrap();
    }
    println!("test_mutex_init_destroy_lock_unlock: PASS");
}

#[test]
fn test_cnd_signal_broadcast_wait() {
    let mtx = Mutex::new(());
    let cnd = Condvar::new();
    {
        let _g = mtx.lock().unwrap();
        cnd.notify_one();
        cnd.notify_all();
    }
    println!("test_cnd_signal_broadcast_wait: PASS (no real waiters)");
}

static ONCE: Once = Once::new();

fn call_once_func() {
    println!("call_once ran");
}

#[test]
fn test_call_once() {
    ONCE.call_once(|| call_once_func());
    println!("test_call_once: PASS");
}