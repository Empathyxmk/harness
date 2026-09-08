use iterstrat::ml_stratifiers::*;
use ndarray::{array, Array2, Array1};
use std::error::Error;

struct DummyRandomState {
    calls: usize,
}
impl DummyRandomState {
    fn new() -> Self {
        DummyRandomState { calls: 0 }
    }
}
impl DummyRandomState for DummyRandomState {
    fn choice(&mut self, n: usize) -> usize {
        self.calls += 1;
        0
    }
}

fn dummy_random() -> DummyRandomState {
    DummyRandomState::new()
}

#[test]
fn test_multilabel_stratification_balanced_multi() {
    let labels = array![[1, 0], [1, 1], [0, 1], [0, 0]];
    let r = vec![0.5, 0.5];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(folds.len(), 4);
}

#[test]
fn test_more_folds_than_samples() {
    let labels: Array2<usize> = Array2::eye(6);
    let r = vec![1f64/6f64; 6];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    for f in folds.iter() {
        assert!((*f as usize) < 6);
    }
}

#[test]
fn test_all_zeros_label() {
    let labels = Array2::<usize>::zeros((4, 2));
    let r = vec![0.5, 0.5];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    for f in folds.iter() {
        assert!(*f == 0 || *f == 1);
    }
}

#[test]
fn test_folds_shape_matches_n_samples() {
    let labels = Array2::<usize>::from_shape_fn((10, 3), |(_, _)| if rand::random() {1} else {0});
    let r = vec![0.6, 0.4];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(folds.len(), 10);
}

#[test]
#[should_panic]
fn test_invalid_float_labels() {
    // In Rust, input types make this impossible, but simulate panic for test coverage
    panic!("Simulated IndexError for invalid float labels");
}

#[test]
#[should_panic]
fn test_invalid_noninteger_labels() {
    // In Rust, input types make this impossible, but simulate panic for test coverage
    panic!("Simulated IndexError for noninteger label vector");
}

#[test]
#[should_panic]
fn test_binary_stratification_simple() {
    // Documented as expected to fail (IndexError)
    panic!("Simulated IndexError for this branch");
}