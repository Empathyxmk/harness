// Translation of operatingsystem_c/chap05_cpu-scheduling/test_pthread_scheduling_extra_public.c

use std::thread;
use std::sync::{Arc, Mutex};
use std::time::Duration;

fn public_test_extra_func(val: Arc<Mutex<i32>>) {
    thread::sleep(Duration::from_millis(5));
    let mut v = val.lock().unwrap();
    *v *= 3;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scheduling_thread3_public() {
        let a = Arc::new(Mutex::new(2));
        let b = Arc::new(Mutex::new(4));
        let c = Arc::new(Mutex::new(8));
        let ta = a.clone();
        let tb = b.clone();
        let tc = c.clone();

        let t1 = std::thread::spawn(move || public_test_extra_func(ta));
        let t2 = std::thread::spawn(move || public_test_extra_func(tb));
        let t3 = std::thread::spawn(move || public_test_extra_func(tc));

        t1.join().unwrap();
        t2.join().unwrap();
        t3.join().unwrap();

        assert_eq!(*a.lock().unwrap(), 6); // 2*3
        assert_eq!(*b.lock().unwrap(), 12); // 4*3
        assert_eq!(*c.lock().unwrap(), 24); // 8*3
    }

    #[test]
    fn test_scheduling_thread4_public() {
        let a = Arc::new(Mutex::new(5));
        let b = Arc::new(Mutex::new(6));
        let c = Arc::new(Mutex::new(7));
        let d = Arc::new(Mutex::new(8));
        let ta = a.clone();
        let tb = b.clone();
        let tc = c.clone();
        let td = d.clone();

        let t1 = std::thread::spawn(move || public_test_extra_func(ta));
        let t2 = std::thread::spawn(move || public_test_extra_func(tb));
        let t3 = std::thread::spawn(move || public_test_extra_func(tc));
        let t4 = std::thread::spawn(move || public_test_extra_func(td));

        t1.join().unwrap();
        t2.join().unwrap();
        t3.join().unwrap();
        t4.join().unwrap();

        assert_eq!(*a.lock().unwrap(), 15);
        assert_eq!(*b.lock().unwrap(), 18);
        assert_eq!(*c.lock().unwrap(), 21);
        assert_eq!(*d.lock().unwrap(), 24);
    }
}