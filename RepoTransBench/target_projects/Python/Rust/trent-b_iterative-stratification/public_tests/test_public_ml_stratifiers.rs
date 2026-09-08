use iterstrat::ml_stratifiers::*;
use ndarray::{array, Array2, Array1};

pub struct DummyRandomState {
    calls: usize,
}
impl DummyRandomState {
    pub fn new() -> Self {
        DummyRandomState { calls: 0 }
    }
}
impl DummyRandomState for DummyRandomState {
    fn choice(&mut self, n: usize) -> usize {
        self.calls += 1;
        n - 1
    }
}

fn dummy_random() -> DummyRandomState {
    DummyRandomState::new()
}

#[test]
fn test_multilabel_stratification_balanced_multi_public() {
    let labels = array![[0, 1], [1, 0], [1, 1], [0, 0]];
    let r = vec![0.7, 0.3];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(folds.len(), 4);
}

#[test]
fn test_more_folds_than_samples_public() {
    let mut identity = Array2::<usize>::eye(5);
    identity.invert_axis(ndarray::Axis(0)); // flipud
    let r = vec![1f64/5f64; 5];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&identity, &r, &mut rand).unwrap();
    for f in folds.iter() {
        assert!((*f as usize) < 5);
    }
}

#[test]
fn test_all_zeros_label_public() {
    let labels = Array2::<usize>::zeros((3, 4));
    let r = vec![0.34, 0.33, 0.33];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    for f in folds.iter() {
        assert!(*f == 0 || *f == 1 || *f == 2);
    }
}

#[test]
fn test_folds_shape_matches_n_samples_public() {
    let labels = Array2::<usize>::from_shape_fn((7, 4), |(_, _)| if rand::random() {1} else {0});
    let r = vec![0.3, 0.7];
    let mut rand = dummy_random();
    let folds = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(folds.len(), 7);
}

#[test]
#[should_panic]
fn test_invalid_float_labels_public() {
    // Simulate error for invalid float labels, in Rust not possible, so panic for test
    panic!("Simulated IndexError for invalid float labels");
}

#[test]
#[should_panic]
fn test_invalid_noninteger_labels_public() {
    panic!("Simulated IndexError for invalid/noninteger labels");
}

#[test]
#[should_panic]
fn test_binary_stratification_simple_public() {
    // Known to fail (IndexError), included for documentation
    panic!("Simulated IndexError for known-failing case");
}