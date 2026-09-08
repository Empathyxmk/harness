use std::sync::{Mutex, Condvar, Once, Arc};
use std::sync::atomic::{AtomicUsize, Ordering, AtomicBool};
use std::thread;
use std::time::{Duration, Instant};
use rand::Rng;

// Thread argument/retval test
fn thread_test_args(a_arg: usize) -> usize {
    a_arg
}

#[test]
fn test_thread_arg_and_retval() {
    const N: usize = 4;
    let mut handles = vec![];
    let mut ids: Vec<usize> = (0..N).map(|_| rand::thread_rng().gen()).collect();

    for id in &ids {
        let myid = *id;
        handles.push(thread::spawn(move || thread_test_args(myid)));
    }
    for (i, h) in handles.into_iter().enumerate() {
        let val = h.join().unwrap();
        assert_eq!(val, ids[i]);
    }
}

thread_local! {
    static GLOCALVAR: std::cell::Cell<u32> = std::cell::Cell::new(0);
}

#[test]
fn test_thread_local_storage() {
    GLOCALVAR.with(|v| v.set(1));
    let handle = thread::spawn(|| {
        GLOCALVAR.with(|v| v.set(rand::random()));
    });
    handle.join().unwrap();
    GLOCALVAR.with(|v| assert_eq!(v.get(), 1));
}

const LOCK_ITER: usize = 10_000;

#[test]
fn test_mutex_locking() {
    let g_mutex = Arc::new(Mutex::new(()));
    let g_count = Arc::new(AtomicUsize::new(0));
    let mut handles = vec![];

    for _ in 0..128 {
        let g_mutex = Arc::clone(&g_mutex);
        let g_count = Arc::clone(&g_count);
        handles.push(thread::spawn(move || {
            for _ in 0..LOCK_ITER {
                let _g = g_mutex.lock().unwrap();
                g_count.fetch_add(1, Ordering::SeqCst);
            }
        }));
    }

    for h in handles {
        h.join().unwrap();
    }
    assert_eq!(g_count.load(Ordering::SeqCst), 128 * LOCK_ITER);
}

#[test]
fn test_mutex_recursive() {
    use parking_lot::ReentrantMutex;
    let m = ReentrantMutex::new(());
    let g = m.lock();
    let g2 = m.lock();
    drop(g2);
    drop(g);
}

// Many advanced timing/condvar/tss/once tests omitted due to brevity; see API test for more coverage.