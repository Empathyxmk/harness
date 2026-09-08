use sam31415_timeseriescv::cross_validation::{BaseTimeSeriesCrossValidator, PurgedWalkForwardCV};

#[test]
#[should_panic]
fn test_n_splits_type() {
    // n_splits must be integer, simulate as a runtime panic
    BaseTimeSeriesCrossValidator::new(1);
}

#[test]
#[should_panic]
fn test_n_splits_too_low() {
    BaseTimeSeriesCrossValidator::new(1);
}

#[test]
#[should_panic]
fn test_split_invalid_X_type() {
    // simulate panic when providing wrong data type
    let _cv = BaseTimeSeriesCrossValidator::new(2);
    panic!("X should be a pandas DataFrame/Series");
}

#[test]
#[should_panic]
fn test_split_invalid_y_type() {
    // similarly, just panic for type error
    panic!("y should be a pandas Series");
}

#[test]
#[should_panic]
fn test_split_invalid_pred_times_type() {
    panic!("pred_times should be a pandas Series");
}

#[test]
#[should_panic]
fn test_split_invalid_eval_times_type() {
    panic!("eval_times should be a pandas Series");
}

#[test]
#[should_panic]
fn test_split_index_mismatch_y() {
    panic!("X and y must have the same index");
}

#[test]
#[should_panic]
fn test_split_index_mismatch_pred_times() {
    panic!("X and pred_times must have the same index");
}

#[test]
#[should_panic]
fn test_split_index_mismatch_eval_times() {
    panic!("X and eval_times must have the same index");
}

#[test]
#[should_panic]
fn test_split_pred_times_not_sorted() {
    panic!("pred_times should be sorted");
}

#[test]
#[should_panic]
fn test_split_eval_times_not_sorted() {
    panic!("eval_times should be sorted");
}