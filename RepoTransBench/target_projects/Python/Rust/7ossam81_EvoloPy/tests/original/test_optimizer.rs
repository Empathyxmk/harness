use std::path::Path;
use std::fs;
use std::process::Command;
use tempfile::TempDir;
use assert_approx_eq::assert_approx_eq;

#[test]
fn test_selector_valid_algorithm() {
    let func_details = vec!["F1".to_string(), "-100".to_string(), "100".to_string(), "30".to_string()];
    let pop_size = 5;
    let iter_count = 2;
    let algo = selector("SSA", &func_details, pop_size, iter_count);  // Assuming selector is implemented
    assert!(algo.is_some());  // Simplified; in full impl, check for attributes
}

#[test]
fn test_selector_invalid_algorithm() {
    let func_details = vec!["F1".to_string(), "-100".to_string(), "100".to_string(), "30".to_string()];
    let result = selector("DoesNotExist", &func_details, 5, 2);
    assert_eq!(result, None);
}

#[test]
fn test_run_function() {
    let tmp_dir = TempDir::new().unwrap();
    let optimizers = vec!["SSA".to_string()];
    let functions = vec!["F1".to_string()];
    let num_runs = 1;
    let params = vec![("PopulationSize", "5"), ("Iterations", "10")];
    let export_flags = vec![true, true, false, false];
    
    run(&optimizers, &functions, num_runs, &params, &export_flags);  // Assuming run is implemented
    
    let timestamp_pattern = regex::Regex::new(r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$").unwrap();
    for entry in fs::read_dir(tmp_dir.path()).unwrap() {
        let dir_name = entry.unwrap().file_name().into_string().unwrap();
        assert!(timestamp_pattern.is_match(&dir_name));
    }
}