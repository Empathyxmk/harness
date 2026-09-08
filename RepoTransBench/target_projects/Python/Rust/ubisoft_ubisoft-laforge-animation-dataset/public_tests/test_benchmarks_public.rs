use ndarray::*;
use crate::benchmarks::*;

#[test]
fn test_fast_npss_simple_public() {
    let mut a = ArrayD::<f64>::zeros(vec![2,12,1]);
    let mut b = ArrayD::<f64>::zeros(vec![2,12,1]);
    for (i, v) in a.iter_mut().enumerate() {
        *v = 1.0 + (i as f64)/24.0;
    }
    for (i, v) in b.iter_mut().enumerate() {
        *v = 2.0 + (i as f64)/24.0;
    }
    let score = fast_npss(&a, &b);
    assert!(!score.is_nan());
    assert!(score.is_finite());
}

#[test]
fn test_fast_npss_different_nan_guard_public() {
    let mut a = ArrayD::<f64>::zeros(vec![2,12,1]);
    let mut b = ArrayD::<f64>::zeros(vec![2,12,1]);
    for (i, v) in a.iter_mut().enumerate() {
        *v = (i as f64)/12.0*3.0;
    }
    for (i, v) in b.iter_mut().enumerate() {
        *v = (i as f64)/12.0*3.0 + 1.0;
    }
    let score = fast_npss(&a, &b);
    assert!(!score.is_nan());
}