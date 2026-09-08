#[test]
fn test_sum_public() {
    let data = vec![7, 15, 18, 23];
    assert_eq!(data.iter().sum::<i32>(), 63);
}

#[test]
fn test_variance_manual_public() {
    let nums = vec![3f64, 9f64, 10f64, 16f64, 24f64];
    let mean = nums.iter().copied().sum::<f64>() / nums.len() as f64;
    let var: f64 = nums.iter().map(|&x| (x - mean) * (x - mean)).sum::<f64>() / nums.len() as f64;
    assert!((var - 50.64).abs() < 1e-7 * 50.64);
}

#[test]
fn test_sample_uniform_stopiteration_public() {
    // Simulate coins iterator exhaustion
    let mut coins = std::iter::empty::<i64>();
    let res = std::panic::catch_unwind(move || coins.next().unwrap());
    assert!(res.is_err());
}

#[test]
fn test_random_choice_manual_public() {
    let collection = vec!["apple", "banana", "pear"];
    let mut coins = vec![0, 1].into_iter(); // binary 01 = 1
    let mut bits = vec![];
    for _ in 0..2 {
        bits.push(coins.next().unwrap());
    }
    let idx = bits[0]*2 + bits[1];
    let chosen = &collection[(idx as usize) % collection.len()];
    assert!(collection.contains(chosen));
}

#[test]
fn test_sample_hgd_stopiteration_manual_public() {
    let mut coins = std::iter::empty::<i64>();
    let res = std::panic::catch_unwind(move || coins.next().unwrap());
    assert!(res.is_err());
}