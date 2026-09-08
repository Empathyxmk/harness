use crate::redbeat::schedules::rrule;

fn test_rrule_basic_init_public() {
    let sched = rrule::new("WEEKLY", Some(8), Some(15));
    format!("{:?}", sched);
    assert_eq!(sched, sched);
}

fn test_rrule_fields_and_eq_public() {
    let s1 = rrule::new("WEEKLY", Some(8), None);
    let s2 = rrule::new("WEEKLY", Some(8), None);
    let s3 = rrule::new("MONTHLY", Some(8), None);
    assert_eq!(s1, s2);
}

fn test_rrule_repr_public() {
    let s = rrule::new("WEEKLY", Some(4), None);
    let r = format!("{:?}", s);
    assert!(r.contains("rrule"));
    assert!(r.contains("byhour"));
}

#[test]
fn test_public_schedules_extra_suite() {
    test_rrule_basic_init_public();
    test_rrule_fields_and_eq_public();
    test_rrule_repr_public();
}