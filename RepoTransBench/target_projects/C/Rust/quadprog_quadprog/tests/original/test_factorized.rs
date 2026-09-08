use approx::assert_abs_diff_eq;
use ndarray::{array, Array1, Array2};

use quadprog_quadprog::solve_qp_factorized;

#[test]
fn test_factorized_qp() {
    let p = array![[2.0, 1.0], [1.0, 2.0]];
    let q = array![-2.0, -6.0];
    let g = array![[1.0, 1.0], [-1.0, 2.0], [2.0, 1.0]];
    let h = array![2.0, 2.0, 3.0];

    let sol = solve_qp_factorized(&p, &q, &g, &h);
    assert_eq!(sol.shape(), &[2]);
    let psq = p.dot(&sol) + &q;
    let gsol_minus_h = &g.dot(&sol) - &h;
    let gsol_minus_h_max = gsol_minus_h.mapv(|x| if x > 0.0 { x } else { 0.0 });
    let lag = &psq + &g.t().dot(&gsol_minus_h_max);
    for elem in lag.iter() {
        assert_abs_diff_eq!(*elem, 0.0, epsilon = 1e-4);
    }
}

#[test]
fn test_unconstrained_factorized() {
    let p = array![[4.0, 2.0], [2.0, 2.0]];
    let q = array![-8.0, -6.0];
    let g = Array2::<f64>::zeros((0, 2));
    let h = Array1::<f64>::zeros(0);

    let sol = solve_qp_factorized(&p, &q, &g, &h);
    let expected_sol = p.solve_into(-&q).unwrap();
    assert_abs_diff_eq!(sol, expected_sol, epsilon = 1e-8);
}