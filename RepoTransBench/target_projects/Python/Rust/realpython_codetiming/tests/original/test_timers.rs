use realpython_codetiming::timers::Timers;

#[test]
fn test_add_and_total_and_count() {
    let mut timers = Timers::new();
    timers.add("t1", 1.0);
    timers.add("t1", 2.0);
    assert_eq!(timers.count("t1"), 2);
    assert_eq!(timers.total("t1"), 3.0);
}

#[test]
fn test_min_max_mean_median_stdev() {
    let mut timers = Timers::new();
    let vals = vec![1.0, 2.0, 3.0];
    for v in &vals {
        timers.add("x", *v);
    }
    assert_eq!(timers.min("x"), *vals.iter().min_by(|a, b| a.partial_cmp(b).unwrap()).unwrap());
    assert_eq!(timers.max("x"), *vals.iter().max_by(|a, b| a.partial_cmp(b).unwrap()).unwrap());
    assert!((timers.mean("x") - (vals.iter().sum::<f64>()/(vals.len() as f64))).abs() < 1e-10);
    assert_eq!(timers.median("x"), 2.0);
    assert!(timers.stdev("x").is_finite());
    assert!(timers.stdev("x") > 0.0);
}

#[test]
fn test_stdev_nan_for_one_entry() {
    let mut timers = Timers::new();
    timers.add("single", 2.345);
    assert!(timers.stdev("single").is_nan());
}

#[test]
#[should_panic]
fn test_apply_keyerror() {
    let timers = Timers::new();
    timers.apply(|v| v.iter().sum(), "not_exist");
}

#[test]
#[should_panic]
fn test_setitem_error() {
    let mut timers = Timers::new();
    timers["bad"] = 5.0;
}

#[test]
fn test_clear() {
    let mut timers = Timers::new();
    timers.add("foo", 1.2);
    timers.clear();
    assert_eq!(timers._timings.len(), 0);
    assert_eq!(timers.data().len(), 0);
}

#[test]
#[should_panic]
fn test_total_no_timings() {
    let timers = Timers::new();
    timers.total("missing");
}

#[test]
fn test_min_max_zero_if_empty() {
    let mut timers = Timers::new();
    timers._timings.insert("e".to_string(), vec![]);
    assert_eq!(timers.min("e"), 0.0);
    assert_eq!(timers.max("e"), 0.0);
}

#[test]
fn test_mean_median_zero_if_empty() {
    let mut timers = Timers::new();
    timers._timings.insert("e".to_string(), vec![]);
    assert_eq!(timers.mean("e"), 0.0);
    assert_eq!(timers.median("e"), 0.0);
}

#[test]
#[should_panic]
fn test_stdev_keyerror_if_missing() {
    let timers = Timers::new();
    timers.stdev("N/A");
}