use crate::trigger::Trigger;

#[test]
fn test_trigger_toggle_and_str() {
    let mut trig = Trigger::new();
    trig.toggle();
    assert!(trig.is_running);
    assert!(format!("{:?}", trig).len() > 0 || format!("{}", trig).len() > 0);
}

#[test]
fn test_trigger_pause_resume() {
    let mut trig = Trigger::new();
    trig.pause();
    assert!(!trig.is_running);
    trig.resume();
    assert!(trig.is_running);
}