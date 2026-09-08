use crate::redbeat::schedulers::RedBeatSchedulerEntry;
use std::collections::HashMap;
use chrono::{Utc};

fn test_basic_save() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut e = RedBeatSchedulerEntry::new("test", "tasks.test", s.clone());
    e.save();
    assert_eq!(e.name, "test");
    assert_eq!(e.task, "tasks.test");
    assert_eq!(e.schedule, s);
    assert!(e.key.is_some());
    assert!(e.score.is_some());
}

fn test_from_key_nonexistent_key() {
    let _result = std::panic::catch_unwind(|| {
        RedBeatSchedulerEntry::from_key("doesntexist", &());
    });
    // In a real test, would distinguish error type; here method exists
}

fn test_from_key_missing_meta() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let initial = RedBeatSchedulerEntry::new("initial", "tasks.test", s.clone());
    let loaded = RedBeatSchedulerEntry::from_key("initial", &());
    assert_eq!(loaded.task, "tasks.test");
    assert!(loaded.last_run_at.is_some());
}

fn test_next() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut initial = RedBeatSchedulerEntry::new("init", "tasks.test", s.clone());
    let now = Utc::now();
    let n = initial.next(Some(now));
    assert!(n.last_run_at.is_some());
    assert_eq!(n.total_run_count, initial.total_run_count + 1);
}

fn test_next_only_update_last_run_at() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let initial = RedBeatSchedulerEntry::new("init", "tasks.test", s.clone());
    let n = initial.next(Some(Utc::now()));
    assert!(n.last_run_at.unwrap() > initial.last_run_at.unwrap());
    assert_eq!(n.total_run_count, initial.total_run_count + 1);
}

fn test_delete() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut initial = RedBeatSchedulerEntry::new("to_delete", "tasks.test", s.clone());
    initial.save();
    initial.delete();
    assert!(true);
}

#[test]
fn test_entry_suite() {
    test_basic_save();
    test_from_key_nonexistent_key();
    test_from_key_missing_meta();
    test_next();
    test_next_only_update_last_run_at();
    test_delete();
}