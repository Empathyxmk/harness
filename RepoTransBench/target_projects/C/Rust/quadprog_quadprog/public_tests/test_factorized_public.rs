use approx::{assert_abs_diff_eq};
use ndarray::{array, Array1, Array2};

use quadprog_quadprog::solve_qp_factorized_full;

#[test]
fn test_qp_factorized_diff_data_public() {
    let p = array![[6.0, 2.0], [2.0, 3.0]];
    let q = array![-4.0, -1.0];
    let g = array![[-1.0, 0.0], [0.0, -1.0], [1.0, 2.0]];
    let h = array![0.0, 0.0, 4.0];

    let (sol, _obj, _active, status) = solve_qp_factorized_full(&p, &q, &g, &h);
    let expected_sol = array![0.0, 2.0];
    assert_abs_diff_eq!(sol, expected_sol, epsilon = 1e-6);
    assert_eq!(status, 0);
}

#[test]
fn test_qp_factorized_interesting_constraint_public() {
    let p = array![[2.0, 0.5], [0.5, 1.0]];
    let q = array![0.0, 0.0];
    let g = array![[-1.0, 0.0], [0.0, -1.0], [1.0, 1.0], [-1.0, 2.0]];
    let h = array![0.0, 0.0, 2.2, 1.5];

    let (sol, _obj, _active, status) = solve_qp_factorized_full(&p, &q, &g, &h);
    assert!(sol[0] >= -1e-8);
    assert!(sol[1] >= -1e-8);
    assert!(sol[0] + sol[1] - 2.2 <= 1e-6);
    assert!(-sol[0] + 2.0 * sol[1] - 1.5 <= 1e-6);
    assert_eq!(status, 0);
}