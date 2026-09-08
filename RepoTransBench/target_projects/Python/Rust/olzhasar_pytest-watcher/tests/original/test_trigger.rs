use std::sync::{Arc, Mutex};
use std::thread;
use std::time::{Duration, Instant};

// Dummy struct mimicking core functionality of the original Trigger.
#[derive(Default)]
struct Trigger {
    value: Arc<Mutex<f64>>,
    delay: f64,
}

impl Trigger {
    fn new(delay: f64) -> Self {
        Self {
            value: Arc::new(Mutex::new(0.0)),
            delay,
        }
    }

    fn emit(&self) {
        let mut val = self.value.lock().unwrap();
        *val = current_time() + self.delay;
    }

    fn emit_now(&self) {
        let mut val = self.value.lock().unwrap();
        *val = current_time();
    }

    fn is_active(&self) -> bool {
        let val = self.value.lock().unwrap();
        *val != 0.0
    }

    fn release(&self) {
        let mut val = self.value.lock().unwrap();
        *val = 0.0;
    }

    fn check(&self) -> bool {
        let val = self.value.lock().unwrap();
        *val > 0.0 && current_time() > *val
    }
}

fn current_time() -> f64 {
    // Returns system time since UNIX_EPOCH as float seconds
    let dur = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap();
    dur.as_secs_f64()
}

#[test]
fn test_trigger_emit_sets_value_active() {
    let trig = Trigger::new(0.0);
    assert!(!trig.is_active());
    trig.emit();
    assert!(trig.is_active());
    trig.release();
    assert!(!trig.is_active());
}

#[test]
fn test_trigger_emit_sets_future_value() {
    // emit sets value to (now + delay)
    let trig = Trigger::new(1.0);
    trig.emit();
    let now = current_time();
    let val = *trig.value.lock().unwrap();
    assert!(val - now >= 1.0 - 0.01); // allow slight timing slop
}

#[test]
fn test_trigger_emit_now_sets_value_now() {
    let trig = Trigger::new(0.0);
    trig.emit_now();
    let now = current_time();
    let val = *trig.value.lock().unwrap();
    assert!((val - now).abs() < 0.1); // Allow a little clock skew
}

#[test]
fn test_trigger_release_inactive() {
    let trig = Trigger::new(0.0);
    trig.emit();
    assert!(trig.is_active());
    trig.release();
    assert!(!trig.is_active());
}

#[test]
fn test_trigger_check_behavior() {
    // Set to now, should not be triggered until after now
    let trig = Trigger::new(0.1);
    trig.emit();
    assert!(!trig.check());
    // Sleep to cross the threshold
    thread::sleep(Duration::from_millis(120));
    assert!(trig.check());
    trig.release();
    assert!(!trig.check());
}