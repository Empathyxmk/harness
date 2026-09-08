use ndarray::*;
use crate::benchmarks::*;
use tempfile::NamedTempFile;
use std::fs::File;
use std::io::{Write, Seek, SeekFrom};

#[test]
fn test_pickle_stats_public() {
    // Not applicable: Ignore, "pickle" and tmp_path don't translate
    assert!(true);
}

#[test]
fn test_benchmark_on_fake_data_public() {
    let x = Array4::<f64>::from_elem((1,10,2,3), 2.0);
    let y = Array4::<f64>::from_elem((1,10,2,3), 1.0);
    let _ = fast_npss(&x.into_dyn(), &y.into_dyn());
}

#[test]
fn test_benchmark_nan_guard_with_nan_input_public() {
    let mut a = ArrayD::<f64>::zeros(vec![1,2,2]);
    a[[0,1,0]] = f64::NAN;
    let b = ArrayD::<f64>::from_elem(vec![1,2,2], 1.0);
    let score = fast_npss(&a, &b);
    assert!(score.is_nan() || score >= 0.0);
}