use sam31415_timeseriescv::cross_validation::{PurgedWalkForwardCV, embargo, BaseTimeSeriesCrossValidator};

#[test]
fn test_purged_walk_forward_cv_nondefault_public() {
    let n_rows = 30;
    let cv = PurgedWalkForwardCV::new(5, 6, 2, 1);
    let splits = cv.split(n_rows);
    assert_eq!(splits.len(), 5);
    assert_eq!(splits[0].0[0], 0);
    assert_eq!(splits.last().unwrap().1.last().unwrap(), &(n_rows - 1));
}

#[test]
fn test_embargo_public() {
    let mut arr = [false; 20];
    embargo(&mut arr, 6, 13, 4);
    assert!(arr[13]);
    assert!(arr[14]);
    assert!(arr[15]);
    assert!(arr[16]);
    assert!(!arr[12]);
}

#[test]
fn test_walkforward_length_public() {
    let n_rows = 34;
    let cv = PurgedWalkForwardCV::new(2, 12, 9, 2);
    let splits = cv.split(n_rows);
    assert_eq!(splits.len(), 2);
    // test indices non-overlapping
    let mut last = -1i32;
    for split in splits.iter() {
        let first_test = *split.1.first().unwrap() as i32;
        assert!(first_test > last);
        last = *split.1.last().unwrap() as i32;
    }
}

#[test]
fn test_repr_public() {
    let cv = PurgedWalkForwardCV::new(3, 8, 3, 3);
    let rp = format!("{}", cv);
    assert!(rp.contains("PurgedWalkForwardCV") && rp.contains("n_splits=3"));
}

#[test]
fn test_cross_validator_base_public() {
    struct DummyCV;
    impl DummyCV {
        fn split(&self, n: usize) -> Vec<(Vec<usize>, Vec<usize>)> {
            // yields one split
            let train: Vec<usize> = (0..n/3).collect();
            let test: Vec<usize> = (n/3..n/2).collect();
            vec![(train, test)]
        }
        fn get_n_splits(&self, _n: usize) -> usize {
            1
        }
    }
    let cv = DummyCV;
    let n = 10;
    let splits = cv.split(n);
    assert_eq!(splits.len(), 1);
    let (train_idx, test_idx) = &splits[0];
    assert!(!train_idx.is_empty());
    assert!(!test_idx.is_empty());
    let tset: std::collections::HashSet<_> = train_idx.iter().cloned().collect();
    let tst: std::collections::HashSet<_> = test_idx.iter().cloned().collect();
    assert!(tset.is_disjoint(&tst));
}

#[test]
fn test_purgedwalkforwardcv_get_n_splits_public() {
    let n_rows = 29;
    let cv = PurgedWalkForwardCV::new(3, 7, 2, 2);
    assert_eq!(cv.get_n_splits(n_rows), 3);
}

#[test]
fn test_split_indices_non_overlap_public() {
    let n_rows = 24;
    let cv = PurgedWalkForwardCV::new(4, 5, 5, 3);
    for (tr, te) in cv.split(n_rows).iter() {
        let tset: std::collections::HashSet<_> = tr.iter().cloned().collect();
        let tst: std::collections::HashSet<_> = te.iter().cloned().collect();
        assert!(tset.is_disjoint(&tst));
    }
}

#[test]
fn test_large_embargo_edge_public() {
    let mut mask = [false; 12];
    embargo(&mut mask, 8, 10, 4);
    assert!(mask[10..].iter().all(|&x| x));
}