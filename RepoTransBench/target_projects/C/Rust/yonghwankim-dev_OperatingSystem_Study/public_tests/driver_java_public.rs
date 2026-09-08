// Translation of operatingsystem_java/src/chap04_01_prime/DriverPublicTest.java

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

    #[test]
    fn public_single_thread_test() {
        let n = 101;
        let mut primes = vec![false; n + 1];
        for i in 1..=n {
            if is_prime(i) {
                primes[i] = true;
            }
        }
        let cnt = primes.iter().filter(|&&p| p).count();
        assert_eq!(cnt, 26, "Number of primes up to 101 should be 26");
    }

    #[test]
    fn public_double_thread_test() {
        let n = 200;
        let primes = Arc::new(Mutex::new(vec![false; n + 1]));
        let p1 = primes.clone();
        let p2 = primes.clone();

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

        let primes = primes.lock().unwrap();
        let cnt = primes.iter().filter(|&&p| p).count();
        assert_eq!(cnt, 46, "Number of primes up to 200 should be 46");
    }

    #[test]
    fn public_triple_thread_test() {
        let n = 500;
        let primes = Arc::new(Mutex::new(vec![false; n + 1]));
        let n1 = n / 3;
        let n2 = (n / 3 + 1) * 2;

        let p1 = primes.clone();
        let p2 = primes.clone();
        let p3 = primes.clone();

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

        let primes = primes.lock().unwrap();
        let cnt = primes.iter().filter(|&&p| p).count();
        assert_eq!(cnt, 95, "Number of primes up to 500 should be 95");
    }
}