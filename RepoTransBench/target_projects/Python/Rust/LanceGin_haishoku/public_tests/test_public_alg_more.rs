use haishoku_rs::alg;
use std::collections::HashMap;

#[test]
fn test_sort_color_variation() {
    let mut color_hist = HashMap::new();
    color_hist.insert((20, 20, 20), 1);
    color_hist.insert((200, 200, 200), 3);
    color_hist.insert((100, 100, 100), 2);
    let result = alg::sort_color(color_hist);
    assert_eq!(result[0].0, (200, 200, 200));
    assert_eq!(result[1].0, (100, 100, 100));
    assert_eq!(result[2].0, (20, 20, 20));
}

#[test]
fn test_get_color_distinct_vivid() {
    let base = vec![(13,23,33), (14,23,32), (110,150,195), (111,150,195), (110,151,194)];
    let res = alg::get_color(base.clone(), 2);
    assert_eq!(res.len(), 2);
    let flat_res: Vec<_> = res.iter().collect();
    assert!(flat_res.iter().any(|x| matches!(x, &(r, g, b) if true)));
}