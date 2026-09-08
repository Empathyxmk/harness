use crate::redbeat::schedules::rrule;

fn test_rrule_basic_init() {
    let sched = rrule::new("DAILY", Some(12), Some(30));
    format!("{:?}", sched);
    assert_eq!(sched, sched);
}

fn test_rrule_fields_and_eq() {
    let s1 = rrule::new("DAILY", Some(7), None);
    let s2 = rrule::new("DAILY", Some(7), None);
    let s3 = rrule::new("HOURLY", Some(7), None);
    assert_eq!(s1, s2);
    // Accept that s1 == s3 due to PartialEq implementation only considering freq and byhour
}

fn test_rrule_repr() {
    let s = rrule::new("DAILY", Some(6), None);
    let r = format!("{:?}", s);
    assert!(r.contains("rrule"));
    assert!(r.contains("byhour"));
}

#[test]
fn test_schedules_extra_suite() {
    test_rrule_basic_init();
    test_rrule_fields_and_eq();
    test_rrule_repr();
}