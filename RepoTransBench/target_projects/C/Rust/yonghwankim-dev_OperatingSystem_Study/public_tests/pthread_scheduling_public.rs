// Translation of operatingsystem_c/chap05_cpu-scheduling/test_pthread_scheduling_public.c

use std::thread;
use std::sync::{Arc, Mutex};
use std::time::Duration;

fn public_test_thread_func(val: Arc<Mutex<i32>>) {
    thread::sleep(Duration::from_millis(20));
    let mut v = val.lock().unwrap();
    *v += 2;
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn test_scheduling_single_thread_public() {
        let result = Arc::new(Mutex::new(5));
        let r = result.clone();
        let t1 = thread::spawn(move || {
            public_test_thread_func(r);
        });
        t1.join().unwrap();
        assert_eq!(*result.lock().unwrap(), 7);
    }

    #[test]
    fn test_scheduling_multi_thread_public() {
        let result1 = Arc::new(Mutex::new(12));
        let result2 = Arc::new(Mutex::new(21));
        let r1 = result1.clone();
        let r2 = result2.clone();

        let t1 = thread::spawn(move || {
            public_test_thread_func(r1);
        });
        let t2 = thread::spawn(move || {
            public_test_thread_func(r2);
        });

        t1.join().unwrap();
        t2.join().unwrap();
        assert_eq!(*result1.lock().unwrap(), 14);
        assert_eq!(*result2.lock().unwrap(), 23);
    }
}