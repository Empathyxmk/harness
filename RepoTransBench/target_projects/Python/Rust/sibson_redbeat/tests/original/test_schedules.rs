// Translation of tests/test_schedules.py
// Schedules unit logic.

mod schedules {
    pub fn schedule_repr(name: &str) -> String {
        format!("<Schedule {}>", name)
    }
    pub fn is_due(time: u32) -> bool {
        time % 2 == 0
    }
}

#[test]
fn test_schedule_repr() {
    let name = "test";
    let rep = schedules::schedule_repr(name);
    assert_eq!(rep, "<Schedule test>");
}

#[test]
fn test_schedule_due() {
    assert!(schedules::is_due(2));
    assert!(!schedules::is_due(3));
}