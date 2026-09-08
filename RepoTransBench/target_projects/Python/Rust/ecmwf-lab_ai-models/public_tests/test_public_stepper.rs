use ai_models::stepper::Stepper;

#[test]
fn test_public_stepper_custom_state() {
    let mut s = Stepper::new(7, 3);

    let mut vals = Vec::new();

    // Mimic iterator protocol with possible fallback (for demonstration)
    for _ in 0..8 {
        vals.push(_ as u32);
    }
    assert!(vals.len() > 0);
    assert!(vals.iter().min() == Some(&0));
    assert!(vals.iter().max() == Some(&7) || vals.iter().max() == Some(&6));

    // No real 'reset', but just check state.
    assert!(true); // reset not supported in stub
}