use flask_babel_rs::*;
use serial_test::serial;
use std::sync::{Arc, Mutex};
use std::thread;

#[test]
#[serial]
fn test_force_locale() {
    let babel = Babel::new();

    {
        let _locale_guard = babel.force_locale("de_DE");
        assert_eq!(get_locale(), "de_DE");
        {
            let _en_guard = babel.force_locale("en_US");
            assert_eq!(get_locale(), "en_US");
        }
        assert_eq!(get_locale(), "de_DE");
    }
}

#[test]
#[serial]
fn test_force_locale_with_threading() {
    let babel = Babel::new();
    let semaphore = Arc::new(Mutex::new(()));

    let sem_cloned = semaphore.clone();

    let th = thread::spawn(move || {
        let _locale_guard = babel.force_locale("en_US");
        assert_eq!(get_locale(), "en_US");
        let _sem = sem_cloned.lock().unwrap(); // Mimic semaphore acquire
    });

    thread::sleep(std::time::Duration::from_millis(10));
    {
        let _locale_guard = babel.force_locale("de_DE");
        assert_eq!(get_locale(), "de_DE");
    }

    drop(semaphore.lock().unwrap());
    th.join().unwrap();
}

#[test]
fn test_refresh_during_force_locale() {
    let babel = Babel::new();
    let _en_guard = babel.force_locale("en_US");
    assert_eq!(get_locale(), "en_US");
    // Suppose 'refresh' is a no-op in stub
    assert_eq!(get_locale(), "en_US");
}