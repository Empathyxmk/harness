// Translated from PublicTestLogger.h

use std::{
    sync::{Arc, Mutex, Condvar},
    thread,
    time::Duration,
};

struct Logger {
    queue: Arc<Mutex<Vec<String>>>,
    stop: Arc<(Mutex<bool>, Condvar)>,
    handle: Option<thread::JoinHandle<()>>,
}

impl Logger {
    fn new() -> Logger {
        let queue = Arc::new(Mutex::new(Vec::new()));
        let stop = Arc::new((Mutex::new(false), Condvar::new()));
        let queue_clone = queue.clone();
        let stop_clone = stop.clone();

        let handle = thread::spawn(move || {
            let queue = queue_clone;
            let stop = stop_clone;
            loop {
                {
                    let mut q = queue.lock().unwrap();
                    while !q.is_empty() {
                        let msg = q.remove(0);
                        print!("{}", msg);
                    }
                }
                // Sleep for short time to avoid busy waiting
                let (lock, cvar) = &*stop;
                let stopped = lock.lock().unwrap();
                if *stopped {
                    break;
                }
                drop(stopped);
                thread::sleep(Duration::from_millis(10));
            }
            // Drain remaining messages
            let mut q = queue.lock().unwrap();
            while !q.is_empty() {
                let msg = q.remove(0);
                print!("{}", msg);
            }
        });
        Logger {
            queue,
            stop,
            handle: Some(handle),
        }
    }

    fn print(&self, msg: &str) {
        let mut q = self.queue.lock().unwrap();
        q.push(msg.to_string());
    }

    fn stop_logger(&mut self) {
        {
            let (lock, cvar) = &*self.stop;
            let mut stopped = lock.lock().unwrap();
            *stopped = true;
            cvar.notify_all();
        }
        if let Some(handle) = self.handle.take() {
            let _ = handle.join();
        }
    }
}

impl Drop for Logger {
    fn drop(&mut self) {
        self.stop_logger();
    }
}

#[test]
fn public_test_logger_basic() {
    let mut logger = Logger::new();
    logger.print("foo\n");
    logger.print("bar\n");
    thread::sleep(Duration::from_millis(80));
    logger.stop_logger();
}

#[test]
fn public_test_logger_destructor_on_unused() {
    let _logger = Logger::new();
    // Destructor is called automatically; should not crash
}

#[test]
fn public_test_logger_multiple() {
    let mut logger = Logger::new();
    logger.print("Alpha\n");
    logger.print("Beta\n");
    thread::sleep(Duration::from_millis(40));
    logger.print("Gamma\n");
    thread::sleep(Duration::from_millis(15));
    logger.stop_logger();
}