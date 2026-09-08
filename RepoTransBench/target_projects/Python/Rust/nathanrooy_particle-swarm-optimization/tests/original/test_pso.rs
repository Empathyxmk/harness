use particle_swarm_optimization::cost_functions;
use particle_swarm_optimization::pso_simple;

#[test]
fn test_minimize_with_sphere_function() {
    let x0 = vec![1.0, 2.0];
    let bounds = [(-5.0, 5.0), (-5.0, 5.0)];
    let (err, pos) =
        pso_simple::minimize(cost_functions::sphere, &x0, &bounds, 4, 15, false);
    assert!(
        err <= cost_functions::sphere(&x0),
        "err={} > sphere(x0)={}",
        err,
        cost_functions::sphere(&x0)
    );
    assert_eq!(pos.len(), x0.len());
}