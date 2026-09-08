#[test]
fn test_thread_safety_of_cache() {
    use std::sync::{Arc, Mutex};
    use std::thread;
    use rand::{thread_rng, seq::SliceRandom};
    let errors: Arc<Mutex<Vec<String>>> = Arc::new(Mutex::new(vec![]));
    let valid_chars = ['a', 'b', 'c']; // Restrict to 3
    let mut rng = thread_rng();
    let expressions: Vec<String> = (0..30).map(|_| {
        valid_chars.choose(&mut thread_rng()).unwrap().to_string().repeat(3)
    }).collect();

    let worker = || {
        for expr in &expressions {
            if expr.len() > 10_000 {
                errors.lock().unwrap().push(format!("ValueError: Sample larger than population ({})", expr.len()));
            }
        }
    };
    let handles: Vec<_> = (0..2).map(|_| {
        let errors = errors.clone();
        thread::spawn(move || worker())
    }).collect();

    for handle in handles {
        handle.join().unwrap();
    }

    let errors = errors.lock().unwrap();
    for error in errors.iter() {
        assert!(!error.contains("Sample larger than population CAPTURE"));
    }
}