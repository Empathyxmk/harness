use iterstrat::ml_stratifiers::*;
use ndarray::{array, Array2};

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

#[test]
fn test_iterative_stratification_varied_public() {
    // Test 1
    let labels = array![[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]];
    let r = vec![0.7, 0.3];
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
fn test_iterative_stratification_varied_expected_index_error_public() {
    let labels = array![[0],[0],[1],[1]];
    let r = vec![0.4, 0.6];
    let _ = iterative_stratification(&labels, &r, &mut DummyRandomState::new()).unwrap();
}

#[test]
fn test_iterative_stratification_all_ones_label_public() {
    let labels = Array2::<usize>::ones((4, 3));
    let r = vec![0.2, 0.4, 0.4];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(out.len(), 4);
}

#[test]
fn test_iterative_stratification_single_fold_public() {
    let labels = Array2::<usize>::eye(5);
    let r = vec![1.0];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    for v in out.iter() {
        assert_eq!(*v, 0);
    }
}

#[test]
fn test_iterative_stratification_random_output_types_public() {
    let labels = array![[0,1],[1,1]];
    let r = vec![0.7, 0.3];
    let mut rs = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rs).unwrap();
    assert_eq!(out.len(), labels.nrows());
}

#[test]
fn test_iterative_stratification_all_zero_labels_branch_public() {
    let labels = Array2::<usize>::zeros((3,5));
    let r = vec![0.2, 0.2, 0.2, 0.2, 0.2];
    let mut rand = DummyRandomState::new();
    let out = iterative_stratification(&labels, &r, &mut rand).unwrap();
    assert_eq!(out.len(), 3);
    for v in out.iter() {
        assert!((*v as usize) < 5);
    }
}