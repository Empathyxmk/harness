// public_tests/bitlock_try_public_test.rs
// Translated from dev/bitlock_try_public_test.c

use noporpoise_bitarray::bitlock::BitLockArray;
use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};
use std::thread;
use std::time::Duration;

#[test]
fn test_bitlock_try_public_acquire() {
    const NWORKERS: usize = 7;
    const LIMIT: usize = 5279;

    let locks = Arc::new(BitLockArray::new(LIMIT));
    let results = Arc::new((0..NWORKERS).map(|_| AtomicUsize::new(0)).collect::<Vec<_>>());
    let mut handles = vec![];
    for wid in 0..NWORKERS {
        let locks_cl = locks.clone();
        let result_cl = results.clone();
        handles.push(thread::spawn(move || {
            for i in 0..LIMIT {
                let locked = locks_cl.try_acquire(i);
                if locked {
                    result_cl[wid].fetch_add(i, Ordering::SeqCst);
                }
                if (i & 0x7f) == 0x7f { thread::sleep(Duration::from_micros(50)); }
            }
        }));
    }
    for h in handles { h.join().unwrap(); }
    let sum: usize = results.iter().map(|r| r.load(Ordering::SeqCst)).sum();
    let expsum = (LIMIT-1)*LIMIT/2;
    assert!(sum >= expsum, "sum={} expsum={}", sum, expsum);
}