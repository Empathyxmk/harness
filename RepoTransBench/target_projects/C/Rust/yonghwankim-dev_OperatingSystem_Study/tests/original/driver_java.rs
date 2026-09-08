// Rust translation NOTE:
// This file represents the test logic of operatingsystem_java/src/chap04_01_prime/DriverTest.java
// Original test uses Java multithreading to find/prinm primes up to 10 million.
// For demo in Rust, the logic will be adapted for comparable thread and computation logic.

use std::thread;

fn is_prime(n: usize) -> bool {
    if n <= 1 {
        return false;
    }
    for i in 2..=((n as f64).sqrt() as usize) {
        if n % i == 0 {
            return false;
        }
    }
    true
}

fn count_primes_single_thread(n: usize) -> usize {
    let mut count = 0;
    for i in 1..=n {
        if is_prime(i) {
            count += 1;
        }
    }
    count
}

fn count_primes_range(primes: &mut [bool], start: usize, end: usize) {
    for i in start..=end {
        if is_prime(i) {
            primes[i] = true;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Mutex};
    use std::thread;

    #[test]
    #[ignore]
    fn single_thread_test() {
        // Corresponds to Java @Disabled; should be run manually
        let n = 10_000_000;
        let mut primes = vec![false; n + 1];
        for i in 1..=n {
            if is_prime(i) {
                primes[i] = true;
            }
        }
        // For demonstration, we won't print all primes here
        let _ = primes;
    }

    #[test]
    #[ignore]
    fn double_thread_test() {
        let n = 10_000_000;
        let primes = Arc::new(Mutex::new(vec![false; n + 1]));
        let p1 = Arc::clone(&primes);
        let p2 = Arc::clone(&primes);

        let t1 = thread::spawn(move || {
            let mut primes = p1.lock().unwrap();
            count_primes_range(&mut primes, 1, n / 2);
        });

        let t2 = thread::spawn(move || {
            let mut primes = p2.lock().unwrap();
            count_primes_range(&mut primes, (n / 2) + 1, n);
        });

        t1.join().unwrap();
        t2.join().unwrap();
        // For demonstration, we don't print primes
    }

    #[test]
    fn third_thread_test() {
        let n = 10_000_000;
        let primes = Arc::new(Mutex::new(vec![false; n + 1]));
        let n1 = n / 3;
        let n2 = (n / 3 + 1) * 2;
        let p1 = Arc::clone(&primes);
        let p2 = Arc::clone(&primes);
        let p3 = Arc::clone(&primes);

        let t1 = thread::spawn(move || {
            let mut primes = p1.lock().unwrap();
            count_primes_range(&mut primes, 1, n1);
        });

        let t2 = thread::spawn(move || {
            let mut primes = p2.lock().unwrap();
            count_primes_range(&mut primes, n1 + 1, n2);
        });

        let t3 = thread::spawn(move || {
            let mut primes = p3.lock().unwrap();
            count_primes_range(&mut primes, n2, n);
        });

        t1.join().unwrap();
        t2.join().unwrap();
        t3.join().unwrap();
        // For demonstration, we don't print primes
    }
}