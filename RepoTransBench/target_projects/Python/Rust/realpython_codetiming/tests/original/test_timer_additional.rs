use realpython_codetiming::timer::{Timer, TimerText, TimerError};
// Panic/assertions in Rust will be used.
use std::rc::Rc;

#[test]
fn test_timer_context_manager_runs() {
    let mut timer = Timer::new("cmmsg", Some(TimerText::Plain("Elapsed time: {0:.4f}s".to_string())), None);
    // Context in Rust: start/stop explicitly
    timer.start().unwrap();
    timer.stop().unwrap();
}

#[test]
fn test_timer_start_stop_elapsed() {
    let mut timer = Timer::new("simple", Some(TimerText::Plain("Time {0:.4f}".to_string())), None);
    assert!(timer._start_time.is_none());
    timer.start().unwrap();
    assert!(timer._start_time.is_some());
    timer.stop().unwrap();
    let elapsed = timer.last;
    assert!(elapsed.is_finite());
}

#[test]
fn test_timer_str_repr() {
    let timer = Timer::new("simple", Some(TimerText::Plain("Time {0:.4f}".to_string())), None);
    let s = format!("{}", timer);
    let rep = format!("{:?}", timer);
    assert!(s.contains("Timer"));
    assert!(rep.contains("Timer"));
}

#[test]
fn test_timer_running_status_via_private() {
    let mut timer = Timer::new("runstat", Some(TimerText::Plain("Running:{0}".to_string())), None);
    timer.start().unwrap();
    assert!(timer._start_time.is_some());
    timer.stop().unwrap();
    assert!(timer._start_time.is_none());
}

#[test]
fn test_timer_logger_callable_text() {
    let messages = Rc::new(std::cell::RefCell::new(vec![]));
    let msg2 = Rc::clone(&messages);
    let logger = Rc::new(move |s: String| {
        msg2.borrow_mut().push(s);
    });
    let cb = Rc::new(|s: f64| format!("Time={:.2}", s));
    let mut timer = Timer::new("cbmsg", Some(TimerText::Function(cb)), Some(logger));
    timer.start().unwrap();
    timer.stop().unwrap();
    let msgs = messages.borrow();
    assert!(!msgs.is_empty());
    assert!(msgs[0].contains("Time="));
}

#[test]
fn test_timer_without_text_logger() {
    let mut timer =
        Timer::new("notext", Some(TimerText::None), None);
    timer.start().unwrap();
    timer.stop().unwrap();
}

#[test]
#[should_panic(expected = "TimerError: Timer is not running")]
fn test_timer_stop_without_start_raises() {
    let mut timer = Timer::new("exception", Some(TimerText::Plain("fail".to_string())), None);
    let _ = timer.stop().unwrap();
}

#[test]
fn test_timer_multiple_starts_raises() {
    let mut timer = Timer::new("multi", Some(TimerText::Plain("multi".to_string())), None);
    timer.start().unwrap();
    let double_start_result = timer.start();
    assert!(double_start_result.is_err());
    timer.stop().unwrap();
}

#[test]
fn test_timer_last_when_nan() {
    let timer = Timer::new("none", Some(TimerText::Plain("none".to_string())), None);
    assert!(timer.last.is_nan());
}

#[test]
fn test_timer_compare_multiple_instances() {
    let timer1 = Timer::new("a", None, None);
    let timer2 = Timer::new("b", None, None);
    // They should not compare as the same.
    assert!(timer1 != timer2);
}