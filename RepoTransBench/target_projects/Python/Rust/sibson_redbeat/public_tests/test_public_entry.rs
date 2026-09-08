use crate::redbeat::schedulers::RedBeatSchedulerEntry;
use chrono::{Utc};

fn test_basic_save_public() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut e = RedBeatSchedulerEntry::new("public_test", "tasks.public_test", s.clone());
    e.save();
    assert_eq!(e.name, "public_test");
    assert_eq!(e.task, "tasks.public_test");
    assert_eq!(e.schedule, s);
    assert!(e.key.is_some());
    assert!(e.score.is_some());
}

fn test_from_key_nonexistent_key_public() {
    let _result = std::panic::catch_unwind(|| {
        RedBeatSchedulerEntry::from_key("doesnotexist_public", &());
    });
}

fn test_from_key_missing_meta_public() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let _initial = RedBeatSchedulerEntry::new("entry_missing_meta", "tasks.public_test", s.clone());
    let loaded = RedBeatSchedulerEntry::from_key("entry_missing_meta", &());
    assert_eq!(loaded.task, "tasks.test");
    assert!(loaded.last_run_at.is_some());
}

fn test_next_public() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut initial = RedBeatSchedulerEntry::new("public_next", "tasks.public_test", s.clone());
    let now = Utc::now();
    let n = initial.next(Some(now));
    assert!(n.last_run_at.is_some());
    assert_eq!(n.total_run_count, initial.total_run_count + 1);
}

fn test_next_only_update_last_run_at_public() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let initial = RedBeatSchedulerEntry::new("public_next_only_update", "tasks.public_test", s.clone());
    let n = initial.next(Some(Utc::now()));
    assert!(n.last_run_at.unwrap() > initial.last_run_at.unwrap());
    assert_eq!(n.total_run_count, initial.total_run_count + 1);
}

fn test_delete_public() {
    let s = crate::redbeat::decoder::DummySchedule::new(3, false);
    let mut initial = RedBeatSchedulerEntry::new("public_delete", "tasks.public_test", s.clone());
    initial.save();
    initial.delete();
    assert!(true);
}

#[test]
fn test_public_entry_suite() {
    test_basic_save_public();
    test_from_key_nonexistent_key_public();
    test_from_key_missing_meta_public();
    test_next_public();
    test_next_only_update_last_run_at_public();
    test_delete_public();
}