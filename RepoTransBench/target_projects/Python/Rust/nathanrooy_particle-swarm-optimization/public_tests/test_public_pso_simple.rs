use particle_swarm_optimization::pso_simple;
use particle_swarm_optimization::pso_simple::Particle;

/// Cost function used for public tests: sum(val^2 for val in x) + 1
fn public_cost(x: &[f64]) -> f64 {
    x.iter().map(|v| v * v).sum::<f64>() + 1.0
}

#[test]
fn test_particle_instance_and_attributes_public() {
    let x0 = vec![7.0, -3.0, 2.0];
    let p = Particle::new(&x0);
    assert_eq!(p.position_i.len(), x0.len());
    assert_eq!(p.velocity_i.len(), x0.len());
    assert_eq!(p.pos_best_i.len(), x0.len());
    let _ = p.err_best_i;
    let _ = p.err_i;
}

#[test]
fn test_particle_evaluate_and_personal_best_public() {
    let x0 = vec![5.0, 6.0];
    let mut p = Particle::new(&x0);
    p.evaluate(&public_cost);
    let err_first = p.err_best_i;

    p.position_i = vec![1.0, 2.0];
    p.evaluate(&public_cost);
    let expected_err = public_cost(&[1.0, 2.0]);
    assert!(p.err_best_i == err_first || p.err_best_i == expected_err);
    assert_eq!(p.err_i, expected_err);
}

#[test]
fn test_particle_update_velocity_and_position_public() {
    let x0 = vec![0.75, -0.25, 0.50];
    let mut p = Particle::new(&x0);
    p.pos_best_i = x0.clone();
    let pos_best_g = vec![0.0, 0.5, -0.5];
    let old_v = p.velocity_i.clone();
    p.update_velocity(&pos_best_g);
    assert_eq!(p.velocity_i.len(), old_v.len());

    let bounds = [(-2.0, 2.0), (-2.0, 2.0), (-2.0, 2.0)];
    // artificially set velocity large to test bounds
    p.velocity_i = vec![3.0, -3.0, 4.0];
    p.update_position(&bounds);
    for v in p.position_i.iter() {
        assert!(*v >= -2.0 && *v <= 2.0);
    }
}

#[test]
fn test_minimize_basic_public() {
    let x0 = vec![2.0, -3.0, 1.0];
    let bounds = [(-7.0, 7.0), (-7.0, 7.0), (-7.0, 7.0)];
    let (err, pos) = pso_simple::minimize(public_cost, &x0, &bounds, 4, 8, false);
    assert!(err.is_finite());
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_minimize_verbose_output_public() {
    let x0 = vec![-1.0, 1.0];
    let bounds = [(-2.0, 2.0), (-2.0, 2.0)];
    let (err, pos) = pso_simple::minimize(public_cost, &x0, &bounds, 3, 2, true);
    assert!(err.is_finite());
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_minimize_edge_case_zero_iterations_public() {
    let x0 = vec![6.0, 8.0];
    let bounds = [(-20.0, 20.0), (-20.0, 20.0)];
    let (err, pos) = pso_simple::minimize(public_cost, &x0, &bounds, 2, 0, false);
    // Accept f64::INFINITY (default), or any finite number
    assert!(err.is_finite() || err == f64::INFINITY);
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_update_position_hits_upper_bound_public() {
    let x0 = vec![0.7, 0.4];
    let mut p = Particle::new(&x0);
    let bounds = [(0.0, 1.0), (0.0, 1.0)];
    // set velocity so position[1] will go above upper bound
    p.velocity_i = vec![0.0, 0.8];
    p.update_position(&bounds);
    assert_eq!(p.position_i[1], 1.0);
    assert_eq!(p.position_i[0], x0[0] + p.velocity_i[0]);
}

#[test]
fn test_update_position_hits_lower_bound_public() {
    let x0 = vec![-0.8, 0.2];
    let mut p = Particle::new(&x0);
    let bounds = [(-1.0, 0.0), (-1.0, 0.0)];
    p.velocity_i = vec![-0.5, 0.0];  // only move the first dimension
    p.update_position(&bounds);
    assert_eq!(p.position_i[0], -1.0);
    assert_eq!(p.position_i[1], x0[1] + p.velocity_i[1]);
}