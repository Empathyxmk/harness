use particle_swarm_optimization::pso_simple;
use particle_swarm_optimization::cost_functions;

#[test]
fn test_minimize_with_sphere_function_public() {
    let x0 = vec![-2.0, 3.0];
    let bounds = [(-10.0, 10.0), (-10.0, 10.0)];
    let (err, pos) =
        pso_simple::minimize(cost_functions::sphere, &x0, &bounds, 5, 12, false);
    assert!(
        err <= cost_functions::sphere(&x0),
        "err={} > sphere(x0)={}",
        err,
        cost_functions::sphere(&x0)
    );
    assert_eq!(pos.len(), x0.len());
}