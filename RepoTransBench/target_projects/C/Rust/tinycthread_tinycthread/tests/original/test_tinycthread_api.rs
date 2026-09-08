use std::sync::{Mutex, Condvar};
use std::sync::atomic::{AtomicI32, Ordering};
use std::thread;
use std::time::{Duration, Instant};

// Helper: thread function which takes arg as mutable, increases it by 1, and returns 42
fn simple_thread(arg: &mut i32) -> i32 {
    *arg += 1;
    42
}

#[test]
fn test_mtx_plain() {
    let m = Mutex::new(());
    {
        let _g = m.lock().unwrap();
    }
    // Mutex with plain semantics: lock/unlock/destroy
}

#[test]
fn test_mtx_recursive() {
    // Rust's Mutex is not recursive. Use ReentrantMutex from parking_lot for recursion.
    use parking_lot::ReentrantMutex;
    use std::sync::Arc;
    let m = Arc::new(ReentrantMutex::new(()));
    let m2 = m.clone();
    let guard = m.lock();
    let guard2 = m2.lock();
    drop(guard2);
    drop(guard);
}

#[test]
fn test_thrd_create_and_join() {
    let mut arg = 10;
    let arg_ptr = std::sync::Arc::new(std::sync::Mutex::new(arg));
    let arg_clone = arg_ptr.clone();
    let handle = thread::spawn(move || {
        let mut data = arg_clone.lock().unwrap();
        *data += 1;
        42
    });
    let res = handle.join().expect("thread panicked");
    let arg_val = *arg_ptr.lock().unwrap();
    assert_eq!(res, 42);
    assert_eq!(arg_val, 11);
}

#[test]
fn test_mtx_trylock() {
    let m = Mutex::new(());
    let g = m.lock().unwrap();
    let try2 = m.try_lock();
    assert!(try2.is_err());
    drop(g);
    let g2 = m.try_lock();
    assert!(g2.is_ok());
}

#[test]
fn test_cnd() {
    let m = Mutex::new(());
    let c = Condvar::new();
    // Condvar signal/broadcast succeeds - no actual waiter in this basic test
    c.notify_one();
    c.notify_all();
}

struct CndWaiterCtx<'a> {
    m: &'a Mutex<bool>,
    c: &'a Condvar,
    value: &'a AtomicI32,
}

fn cnd_waiter_thread(ctx: CndWaiterCtx) {
    let mut guard = ctx.m.lock().unwrap();
    while ctx.value.load(Ordering::SeqCst) == 0 {
        guard = ctx.c.wait(guard).unwrap();
    }
}

#[test]
fn test_cnd_signal_wait() {
    let m = Mutex::new(());
    let c = Condvar::new();
    let done = AtomicI32::new(0);

    let ctx = CndWaiterCtx {
        m: &m,
        c: &c,
        value: &done,
    };

    let waiter = {
        let ctx = CndWaiterCtx {
            m: ctx.m,
            c: ctx.c,
            value: ctx.value,
        };
        thread::spawn(move || cnd_waiter_thread(ctx))
    };

    thread::sleep(Duration::from_millis(10));
    {
        let _guard = m.lock().unwrap();
        done.store(1, Ordering::SeqCst);
        c.notify_one();
    }
    waiter.join().unwrap();
}