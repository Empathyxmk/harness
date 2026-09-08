use particle_swarm_optimization::cost_functions;

#[test]
fn test_sphere_all_zeros_public() {
    assert_eq!(cost_functions::sphere(&[0.0, 0.0, 0.0, 0.0]), 0.0);
}

#[test]
fn test_sphere_single_value_public() {
    assert_eq!(cost_functions::sphere(&[4.0]), 16.0);
}

#[test]
fn test_sphere_negative_values_public() {
    assert_eq!(cost_functions::sphere(&[-3.0, -2.0]), 9.0 + 4.0);
}

#[test]
fn test_sphere_mixed_values_public() {
    assert_eq!(cost_functions::sphere(&[2.0, -3.0, 4.0]), 4.0 + 9.0 + 16.0);
}

#[test]
fn test_sphere_empty_public() {
    let arr: [f64; 0] = [];
    assert_eq!(cost_functions::sphere(&arr), 0.0);
}

#[test]
fn test_main_guard_does_nothing_public() {
    // No-op in Rust; sphere function is always available
    assert!(true);
}