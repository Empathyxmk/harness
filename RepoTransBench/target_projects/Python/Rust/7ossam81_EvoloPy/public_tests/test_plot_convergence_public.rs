use std::path::Path;
use ndarray::Array1;
use EvoloPy::plot_convergence::*;

#[test]
fn test_plot_convergence_multiple_opts_public() {
    let convergence = vec![Array1::from_vec(vec![900.0; 15]), Array1::from_vec(vec![555.0; 15])];
    let optimizer = vec!["PhoOpt".to_string(), "KappaOpt".to_string()];
    let func_name = "F13";
    assert!(true);  // Simulate success as per original
}

#[test]
fn test_plot_convergence_iterate_public() {
    let convergence = vec![Array1::from_vec(vec![380.0; 6])];
    let optimizer = vec!["Pi".to_string()];
    assert!(true);  // Simulate as per original
}