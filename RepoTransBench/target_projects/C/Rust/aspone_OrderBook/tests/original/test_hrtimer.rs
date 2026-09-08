// Translated from TestHRTimer.h

use std::thread::sleep;
use std::time::{Duration, Instant};

struct HRTimer {
    started: Option<Instant>,
    elapsed: u64,
    stopped: bool,
}

impl HRTimer {
    fn new() -> Self {
        HRTimer {
            started: None,
            elapsed: 0,
            stopped: false,
        }
    }
    fn start(&mut self) {
        self.started = Some(Instant::now());
        self.stopped = false;
    }
    fn stop(&mut self) -> u64 {
        if self.stopped {
            return 0;
        }
        let elapsed = if let Some(start) = self.started.take() {
            let duration = start.elapsed();
            let micros = duration.as_micros() as u64;
            self.elapsed = micros;
            self.stopped = true;
            micros
        } else {
            0
        };
        elapsed
    }
    fn get_elapsed(&self) -> u64 {
        self.elapsed
    }
}

#[test]
fn test_hrtimer_basic() {
    let mut t = HRTimer::new();
    t.start();
    sleep(Duration::from_micros(1000)); // 1 ms
    let elapsed = t.stop();
    assert!(elapsed > 0);
    assert_eq!(t.get_elapsed(), elapsed);
}

#[test]
fn test_hrtimer_double_stop() {
    let mut t = HRTimer::new();
    t.start();
    sleep(Duration::from_micros(500)); // 0.5 ms
    let first = t.stop();
    let second = t.stop();
    assert!(first > 0);
    assert_eq!(second, 0);
}

#[test]
fn test_hrtimer_no_start() {
    let mut t = HRTimer::new();
    let elapsed = t.stop(); // Should be 0
    assert_eq!(elapsed, 0);
}