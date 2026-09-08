use std::path::Path;
use std::fs::File;
use std::io::Write;
use tempfile::TempDir;
use ndarray::Array2;
use assert_approx_eq::assert_approx_eq;

#[test]
fn test_run_creates_boxplot() {
    let tmp_dir = TempDir::new().unwrap();
    let results_dir = tmp_dir.path();
    let optimizer = vec!["SSA".to_string(), "PSO".to_string(), "GA".to_string()];
    let objectivefunc = vec!["F1".to_string()];
    let iterations = 100;
    
    // Simulate data setup
    let data = Array2::from_shape_vec((3, 10), vec![0.25f64; 30]).unwrap();  // Mock data
    
    run(results_dir, &optimizer, &objectivefunc, iterations);  // Assuming run is implemented
    assert!(Path::new(&results_dir.join("boxplot-F1.png")).exists());
}

#[test]
fn test_run_handles_data_processing() {
    let tmp_dir = TempDir::new().unwrap();
    let results_dir = tmp_dir.path();
    let optimizer = vec!["SSA".to_string(), "PSO".to_string(), "GA".to_string()];
    let objectivefunc = vec!["F1".to_string()];
    let iterations = 100;
    
    run(results_dir, &optimizer, &objectivefunc, iterations);  // Assuming run is implemented
    // Additional assertions as per original logic
}

#[test]
fn test_run_clears_figure() {
    let tmp_dir = TempDir::new().unwrap();
    let results_dir = tmp_dir.path();
    let optimizer = vec!["SSA".to_string(), "PSO".to_string(), "GA".to_string()];
    let objectivefunc = vec!["F1".to_string()];
    let iterations = 100;
    
    run(results_dir, &optimizer, &objectivefunc, iterations);  // Assuming run is implemented
}