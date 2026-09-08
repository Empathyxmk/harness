use ai_models::stepper::Stepper;

#[test]
fn test_stepper_basic() {
    let mut s = Stepper::new(2, 6);
    assert_eq!(s.num_steps, 3);
    s.start();
    s.call(0, 2);
    s.call(1, 2);
    s.call(2, 2);
    // Note: log output is printed on Drop.
    // For now, we trust Drop prints Elapsed and Average.
}

#[test]
fn test_stepper_zero_steps() {
    let mut s = Stepper::new(5, 0);
    s.start();
    // Drop (at end) should not panic or print average per step.
}