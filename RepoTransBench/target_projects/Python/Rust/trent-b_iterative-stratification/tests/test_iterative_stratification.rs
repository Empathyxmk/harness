use iterstrat::ml_stratifiers::*;
use ndarray::{array, Array2, Array1};

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

#[test]
fn test_iterative_stratification_varied() {
    // Test 1
    let labels = array![[1,0,1],[1,1,0],[0,1,1],[1,0,0],[0,0,0]];
    let r = vec![0.6, 0.4];
    let expected_num_folds = 2;
    let mut rs = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rs).unwrap();
    assert_eq!(out.len(), labels.nrows());
    for v in out.iter() {
        assert!(*v < expected_num_folds);
    }
}

#[test]
#[should_panic]
fn test_iterative_stratification_varied_expected_index_error() {
    let labels = array![[1],[1],[1],[0]];
    let r = vec![0.5, 0.5];
    let expected_num_folds = 2;
    let mut rs = DummyRandomState::new();
    let _ = iterative_stratification(&labels, &r, &mut rs).unwrap();
}

#[test]
fn test_iterative_stratification_all_ones_label() {
    let labels = Array2::<usize>::ones((5, 2));
    let r = vec![0.4, 0.6];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(out.len(), 5);
}

#[test]
fn test_iterative_stratification_single_fold() {
    let labels = Array2::<usize>::eye(4);
    let r = vec![1.0];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    for v in out.iter() {
        assert_eq!(*v, 0);
    }
}

#[test]
fn test_iterative_stratification_random_output_types() {
    let labels = array![[1,0],[1,1]];
    let r = vec![0.5, 0.5];
    let mut rs = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rs).unwrap();
    // Type checks via Rust's strong typing, so just check it's Array1<usize>, already enforced
    assert_eq!(out.len(), labels.nrows());
}

#[test]
fn test_iterative_stratification_all_zero_labels_branch() {
    let labels = Array2::<usize>::zeros((4,2));
    let r = vec![0.25, 0.25, 0.25, 0.25];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(out.len(), 4);
    for v in out.iter() {
        assert!((*v as usize) < 4);
    }
}