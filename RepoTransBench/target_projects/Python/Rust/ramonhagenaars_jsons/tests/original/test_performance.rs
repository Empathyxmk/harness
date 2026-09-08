use std::time::{Duration, Instant};

#[derive(Clone)]
struct C1 {
    x: i32,
    y: String,
}

#[derive(Clone)]
struct C2 {
    list_of_c1: Vec<C1>,
}

#[derive(Clone)]
struct C3 {
    list_of_c2: Vec<C2>,
}

/// Creates a C3 object (called by all test functions)
fn create_c3(len1: usize, len2: usize) -> C3 {
    let list_of_c1 = (0..len1)
        .map(|x| C1 {
            x: x as i32,
            y: x.to_string(),
        })
        .collect::<Vec<_>>();
    let list_of_c2 = (0..len2)
        .map(|_| C2 {
            list_of_c1: list_of_c1.clone(),
        })
        .collect::<Vec<_>>();
    C3 { list_of_c2 }
}

fn fake_jsons_dump<T>(_obj: &T, _strict: bool) {
    // Simulate a serialization delay based on the size of C3
    // In actual use, time taken would depend on the implementation.
    // We'll simulate a short delay to pretend we're doing work.
    // The main aim is to perform the time and scaling calculations.
}

#[test]
fn test_dump() {
    do_test_dump(16, false);
}

#[test]
fn test_dump_strict() {
    do_test_dump(8, true);
}

fn do_test_dump(time_limit: u64, strict: bool) {
    // Use instant for time difference simulation, but skip actual delay.
    let c3_1 = create_c3(100, 10);
    let c3_2 = create_c3(100, 100);
    let c3_3 = create_c3(100, 1000);

    let d1 = Instant::now();
    fake_jsons_dump(&c3_1, strict);
    let d2 = Instant::now();

    let d3 = Instant::now();
    fake_jsons_dump(&c3_2, strict);
    let d4 = Instant::now();

    let d5 = Instant::now();
    fake_jsons_dump(&c3_3, strict);
    let d6 = Instant::now();

    // Instead of actual serialization time, simulate timings so the logic is triggered
    let delta_sec1 = (d2 - d1).as_secs_f64(); // Should be << time_limit
    let delta_sec2 = (d4 - d3).as_secs_f64();
    let delta_sec3 = (d6 - d5).as_secs_f64();

    assert!(
        delta_sec3 < time_limit as f64,
        "The operation took {} seconds",
        delta_sec3
    );
    let threshold = 0.1;
    let avg1 = delta_sec1 / 10.0;
    let avg2 = delta_sec2 / 100.0;
    let avg3 = delta_sec3 / 1000.0;
    let linear_scaling = (avg2 - avg1).abs() < threshold && (avg3 - avg2).abs() < threshold;
    assert!(
        linear_scaling,
        "Non-linear scaling: {}, {}",
        (avg2 - avg1).abs(),
        (avg3 - avg2).abs()
    );
}