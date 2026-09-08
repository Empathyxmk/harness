// public_tests/bitlock_public_test.rs
// Translated from dev/bitlock_public_test.c

use noporpoise_bitarray::bitlock::BitLockArray;
use parking_lot::Mutex;
use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};
use std::thread;
use std::time::Duration;

fn bitlock_worker(locks: Arc<BitLockArray>, data: Arc<Vec<Mutex<u8>>>, id: usize, num_loops: usize, result: &Arc<AtomicUsize>) {
    for i in 0..num_loops {
        while !locks.try_acquire(i) {} // spinlock
        {
            let mut v = data[i].lock();
            result.fetch_add(i + *v as usize, Ordering::SeqCst);
            *v = id as u8;
            drop(v);
            thread::sleep(Duration::from_micros(4));
        }
        // Would release lock
    }
}

#[test]
fn test_bitlock_public_parallel() {
    const NUM_LOOPS: usize = 1234;
    let locks = Arc::new(BitLockArray::new(NUM_LOOPS));
    let data = Arc::new((0..NUM_LOOPS).map(|_| Mutex::new(0u8)).collect::<Vec<_>>());
    let mut handles = vec![];
    let mut results = vec![];
    for id in 0..12 {
        let result = Arc::new(AtomicUsize::new(0));
        let locks_cl = locks.clone();
        let data_cl = data.clone();
        let res_cl = result.clone();
        handles.push(thread::spawn(move || {
            bitlock_worker(locks_cl, data_cl, id+2, NUM_LOOPS, &res_cl)
        }));
        results.push(result);
    }
    for h in handles { h.join().unwrap(); }
    let sum: usize = results.iter().map(|r| r.load(Ordering::SeqCst)).sum();
    assert!(sum > 0);
}