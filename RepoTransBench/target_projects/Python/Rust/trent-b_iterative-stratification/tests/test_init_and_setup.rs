use std::path::Path;

#[test]
fn test_readme_exists() {
    let p = Path::new(env!("CARGO_MANIFEST_DIR")).join("README.md");
    assert!(p.exists());
}

#[test]
fn test_license_exists() {
    let p = Path::new(env!("CARGO_MANIFEST_DIR")).join("LICENSE");
    assert!(p.exists());
}

#[test]
fn test_import_ml_stratifiers() {
    // Simulate "import" by confirming the function is callable
    use iterstrat::ml_stratifiers::iterative_stratification;
    // Test the existence of a function
    let f = iterative_stratification as fn(&ndarray::Array2<usize>, &[f64], &mut dyn iterstrat::ml_stratifiers::DummyRandomState)
        -> Result<ndarray::Array1<usize>, Box<dyn std::error::Error>>;
    let _ = f;
}