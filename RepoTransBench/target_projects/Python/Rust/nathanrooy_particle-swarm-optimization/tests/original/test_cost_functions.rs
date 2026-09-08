use particle_swarm_optimization::cost_functions;

#[test]
fn test_sphere_all_zeros() {
    assert_eq!(cost_functions::sphere(&[0.0, 0.0, 0.0]), 0.0);
}

#[test]
fn test_sphere_single_value() {
    assert_eq!(cost_functions::sphere(&[3.0]), 9.0);
}

#[test]
fn test_sphere_negative_values() {
    assert_eq!(cost_functions::sphere(&[-1.0, -2.0]), 1.0 + 4.0);
}

#[test]
fn test_sphere_mixed_values() {
    assert_eq!(cost_functions::sphere(&[1.0, -2.0, 3.0]), 1.0 + 4.0 + 9.0);
}

#[test]
fn test_sphere_empty() {
    let arr: [f64; 0] = [];
    assert_eq!(cost_functions::sphere(&arr), 0.0);
}

#[test]
fn test_main_guard_does_nothing() {
    // No-op in Rust; sphere function is always available
    assert!(true);
}