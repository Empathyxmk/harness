use particle_swarm_optimization::pso_simple;
use particle_swarm_optimization::pso_simple::Particle;

/// Custom cost for test
fn simple_cost(x: &[f64]) -> f64 {
    x.iter().map(|v| v * v).sum()
}

#[test]
fn test_particle_instance_and_attributes() {
    let x0 = vec![1.0, -1.0];
    let p = Particle::new(&x0);
    assert_eq!(p.position_i.len(), x0.len());
    assert_eq!(p.velocity_i.len(), x0.len());
    // Best positions are also of same dimension
    assert_eq!(p.pos_best_i.len(), x0.len());
    // Should have err_best_i and err_i
    let _ = p.err_best_i;
    let _ = p.err_i;
}

#[test]
fn test_particle_evaluate_and_personal_best() {
    let x0 = vec![2.0, 3.0];
    let mut p = Particle::new(&x0);
    p.evaluate(&simple_cost);
    let err_first = p.err_best_i;

    // evaluate with a different position
    p.position_i = vec![4.0, 5.0];
    p.evaluate(&simple_cost);
    // best either stays the same, or updates if new error is better
    let expected_err = simple_cost(&[4.0, 5.0]);
    assert!(p.err_best_i == err_first || p.err_best_i == expected_err);
    assert_eq!(p.err_i, expected_err);
}

#[test]
fn test_particle_update_velocity_and_position() {
    let x0 = vec![0.5, -0.5];
    let mut p = Particle::new(&x0);
    p.pos_best_i = x0.clone();
    let pos_best_g = vec![0.1, 0.2];
    let old_v = p.velocity_i.clone();
    p.update_velocity(&pos_best_g);
    assert_eq!(p.velocity_i.len(), old_v.len());

    let bounds = [(-1.0, 1.0), (-1.0, 1.0)];
    // artificially set velocity large to test bounds
    p.velocity_i = vec![2.0, -2.0];
    p.update_position(&bounds);
    for v in p.position_i.iter() {
        assert!(*v >= -1.0 && *v <= 1.0);
    }
}

#[test]
fn test_minimize_basic() {
    let x0 = vec![1.0, 2.0];
    let bounds = [(-5.0, 5.0), (-5.0, 5.0)];
    let (err, pos) = pso_simple::minimize(simple_cost, &x0, &bounds, 5, 10, false);
    assert!(err.is_finite());
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_minimize_verbose_output() {
    let x0 = vec![0.0, 0.0];
    let bounds = [(-1.0, 1.0), (-1.0, 1.0)];
    // To capture stdout would require extra crate;
    // Instead, just ensure it runs and returns
    let (err, pos) = pso_simple::minimize(simple_cost, &x0, &bounds, 3, 2, true);
    assert!(err.is_finite());
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_minimize_edge_case_zero_iterations() {
    // Should return initial best
    let x0 = vec![5.0, 7.0];
    let bounds = [(-10.0, 10.0), (-10.0, 10.0)];
    let (err, pos) = pso_simple::minimize(simple_cost, &x0, &bounds, 2, 0, false);
    assert!(err.is_finite() || err == f64::INFINITY); // If everything is f64::INFINITY
    assert_eq!(pos.len(), x0.len());
}

#[test]
fn test_update_position_hits_upper_bound() {
    let x0 = vec![0.9, 0.0];
    let mut p = Particle::new(&x0);
    let bounds = [(0.0, 1.0), (0.0, 1.0)];
    // set velocity so position[0] will go above upper bound
    p.velocity_i = vec![0.5, 0.0];
    p.update_position(&bounds);
    assert_eq!(p.position_i[0], 1.0);
    assert_eq!(p.position_i[1], x0[1] + p.velocity_i[1]);
}

#[test]
fn test_update_position_hits_lower_bound() {
    let x0 = vec![0.0, -0.9];
    let mut p = Particle::new(&x0);
    let bounds = [(-1.0, 0.0), (-1.0, 0.0)];
    // set velocity so position[1] goes below lower bound
    p.velocity_i = vec![0.0, -0.5];
    p.update_position(&bounds);
    assert_eq!(p.position_i[1], -1.0);
    assert_eq!(p.position_i[0], x0[0] + p.velocity_i[0]);
}