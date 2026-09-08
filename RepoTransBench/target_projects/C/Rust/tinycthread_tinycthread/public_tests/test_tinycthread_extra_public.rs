use std::sync::{Mutex, Condvar, Once, Arc};
use std::thread;
use std::sync::atomic::{AtomicI32, Ordering};

fn thread_func_pub(val: &Arc<AtomicI32>) -> i32 {
    val.fetch_add(2, Ordering::SeqCst);
    9
}

#[test]
fn test_thread_start_stop_pub() {
    let val = Arc::new(AtomicI32::new(8));
    let val_clone = val.clone();
    let handle = thread::spawn(move || thread_func_pub(&val_clone));
    let retval = handle.join().unwrap();
    assert_eq!(val.load(Ordering::SeqCst), 10);
    assert_eq!(retval, 9);
    println!("test_thread_start_stop_pub: PASS");
}

#[test]
fn test_mutex_init_destroy_lock_unlock_pub() {
    let mtx = Mutex::new(());
    for _ in 0..2 {
        let _g = mtx.lock().unwrap();
    }
    println!("test_mutex_init_destroy_lock_unlock_pub: PASS");
}

#[test]
fn test_cnd_signal_broadcast_wait_pub() {
    let cnd = Condvar::new();
    let mtx = Mutex::new(());
    cnd.notify_all();
    println!("test_cnd_signal_broadcast_wait_pub: PASS (no real waiters)");
}

static ONCEPUB: Once = Once::new();
static CALLED_PUB: AtomicI32 = AtomicI32::new(0);

fn callback_once_pub() {
    CALLED_PUB.fetch_add(2, Ordering::SeqCst);
}

#[test]
fn test_call_once_pub() {
    CALLED_PUB.store(0, Ordering::SeqCst);
    ONCEPUB.call_once(callback_once_pub);
    assert_eq!(CALLED_PUB.load(Ordering::SeqCst), 2);
    // Second call will not run the callback
    ONCEPUB.call_once(callback_once_pub);
    assert_eq!(CALLED_PUB.load(Ordering::SeqCst), 2);
    println!("call_once_pub ran");
    println!("test_call_once_pub: PASS");
}