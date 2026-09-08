use approx::{assert_abs_diff_eq};
use ndarray::{array, Array1, Array2};

use quadprog_quadprog::solve_qp_full;

#[test]
fn test_qp_simple_public() {
    let p = array![[2.5, 1.0], [1.0, 2.0]];
    let q = array![-2.0, -5.0];
    let g = array![[-1.0, 0.0], [0.0, -1.0], [2.0, 1.0]];
    let h = array![0.0, 0.0, 4.0];

    let (sol, _obj, _active, status) = solve_qp_full(&p, &q, &g, &h);
    let expected_sol = array![1.2, 1.6];
    assert_abs_diff_eq!(sol, expected_sol, epsilon = 1e-5);
    assert_eq!(status, 0);
}

#[test]
fn test_qp_nontrivial_constraints_public() {
    let p = array![[1.0, 0.2], [0.2, 1.0]];
    let q = array![-1.0, -2.0];
    let g = array![[-1.0, 0.0], [0.0, -1.0], [2.0, 1.0]];
    let h = array![0.0, 0.0, 3.5];

    let (sol, _obj, _active, status) = solve_qp_full(&p, &q, &g, &h);
    assert!(sol[0] >= -1e-8);
    assert!(sol[1] >= -1e-8);
    assert!(2.0 * sol[0] + sol[1] - 3.5 <= 1e-6);
    assert_eq!(status, 0);
}