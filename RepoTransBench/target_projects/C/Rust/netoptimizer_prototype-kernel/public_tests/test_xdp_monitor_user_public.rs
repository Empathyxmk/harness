// Simulated monitoring function for public test case.
// Replace with actual logic under test if available.
fn monitor_event_count(start: i32, increment: i32, times: i32) -> i32 {
    let mut count = start;
    for _ in 0..times {
        count += increment;
    }
    count
}

#[test]
fn public_monitor_event_count() {
    // PUBLIC TEST CASES (with different input values)
    let events1 = monitor_event_count(5, 2, 50);   // Start at 5, increment by 2, 50 times
    let events2 = monitor_event_count(20, 3, 10);  // Start at 20, increment by 3, 10 times
    let events3 = monitor_event_count(100, 0, 0);  // Start at 100, increment zero, zero ops

    assert_eq!(events1, 5 + 2*50);    // 105
    assert_eq!(events2, 20 + 3*10);   // 50
    assert_eq!(events3, 100);         // 100

    // Negative case: large decrement
    let events4 = monitor_event_count(50, -5, 15); // 50 + (-5)*15 = -25
    assert_eq!(events4, -25);
}