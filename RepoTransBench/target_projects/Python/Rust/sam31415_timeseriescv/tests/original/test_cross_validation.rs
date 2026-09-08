use sam31415_timeseriescv::cross_validation::{
    BaseTimeSeriesCrossValidator, PurgedWalkForwardCV, CombPurgedKFoldCV,
    purge, embargo, compute_fold_bounds,
};

fn make_simple_data(n: usize) -> (Vec<Vec<f64>>, Vec<u32>) {
    let data = (0..n)
        .map(|i| vec![(i as f64)/n as f64, ((i + 1) as f64)/n as f64, ((i + 2) as f64)/n as f64])
        .collect();
    let labels = (0..n).map(|i| (i%2) as u32).collect();
    (data, labels)
}

#[test]
fn test_base_timeseriescv_n_splits_property() {
    let mut cv = BaseTimeSeriesCrossValidator::new(5);
    assert_eq!(cv.n_splits, 5);
    cv.set_n_splits(6);
    assert_eq!(cv.n_splits, 6);
}

#[test]
fn test_purge_basic_object() {
    let cv = BaseTimeSeriesCrossValidator::new(2);
    let in_train = purge(&cv, 4, 5, 5);
    assert!(in_train.is_empty() || in_train.iter().all(|i| i < 4 || *i > 5));
}

#[test]
fn test_embargo_basic_object() {
    let mut arr = [false; 10];
    embargo(&mut arr, 0, 7, 2);
    // 7,8 should be true
    assert!(arr[7]);
    assert!(arr[8]);
    assert!(!arr[6] && !arr[9]);
}

#[test]
fn test_compute_fold_bounds_object() {
    let cv = BaseTimeSeriesCrossValidator::new(2);
    let bounds = compute_fold_bounds(&cv, false);
    assert!(!bounds.is_empty());
}

#[test]
fn test_purgedwalkforwardcv_split() {
    let (X, y) = make_simple_data(20);
    let cv = PurgedWalkForwardCV::new(5, 2, 1, 0);
    let splits = cv.split(X.len());
    assert_eq!(splits.len(), 5);
    for (train, test) in splits.iter() {
        // No overlap
        let train_set: std::collections::HashSet<_> = train.iter().cloned().collect();
        let test_set: std::collections::HashSet<_> = test.iter().cloned().collect();
        assert!(train_set.is_disjoint(&test_set));
        assert!(!test.is_empty());
    }
}

#[test]
fn test_combpurgedkfoldcv_split() {
    let (X, _y) = make_simple_data(12);
    let cv = CombPurgedKFoldCV::new(3);
    let splits = cv.split(X.len());
    assert_eq!(splits.len(), 3);
    for (train, test) in splits.iter() {
        let train_set: std::collections::HashSet<_> = train.iter().cloned().collect();
        let test_set: std::collections::HashSet<_> = test.iter().cloned().collect();
        assert!(train_set.is_disjoint(&test_set));
    }
}

#[test]
fn test_repr_methods() {
    let cv1 = PurgedWalkForwardCV::new(4, 2, 1, 0);
    let cv2 = CombPurgedKFoldCV::new(3);
    let r1 = format!("{:?}", cv1);
    let r2 = format!("{:?}", cv2);
    assert!(r1.contains("PurgedWalkForwardCV"));
    assert!(r2.contains("CombPurgedKFoldCV"));
}

#[test]
fn test_base_repr() {
    let cv = BaseTimeSeriesCrossValidator::new(10);
    let r = format!("{:?}", cv);
    assert!(r.contains("BaseTimeSeriesCrossValidator"));
}

#[test]
#[should_panic]
fn test_purge_empty_object() {
    let cv = BaseTimeSeriesCrossValidator::new(2);
    // Intentionally trigger panic by using indices out of bounds in `purge` (simulate IndexError)
    let _ = purge(&cv, 100, 100, 100);
}

#[test]
fn test_embargo_no_embargo_object() {
    let mut arr = [false; 5];
    embargo(&mut arr, 0, 2, 0);
    // should leave unchanged
    assert!(!arr.iter().any(|&v| v));
}

#[test]
#[should_panic]
fn test_purgedwalkforwardcv_invalid_n_test_splits() {
    // Simulate ValueError for invalid n_test_splits
    let _ = PurgedWalkForwardCV::new(2, 2, 2, 0);
}

#[test]
#[should_panic]
fn test_combpurgedkfoldcv_invalid() {
    let _ = CombPurgedKFoldCV::new(1);
}