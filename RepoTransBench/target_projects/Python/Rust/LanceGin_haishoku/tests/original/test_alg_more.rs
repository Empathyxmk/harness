use haishoku_rs::alg;

#[test]
fn test_sort_by_rgb_basic() {
    let colors = vec![(10, (52, 150, 70)), (4, (200, 100, 30)), (7, (100, 120, 140))];
    let result = alg::sort_by_rgb(&colors);
    assert_eq!(result, vec![(10, (52, 150, 70)), (7, (100, 120, 140)), (4, (200, 100, 30))]);
}

#[test]
fn test_rgb_maximum_basic() {
    let colors = vec![(2, (10, 20, 30)), (5, (40, 50, 60)), (3, (25, 35, 45))];
    let result = alg::rgb_maximum(&colors);
    assert_eq!(*result.get("r_max").unwrap(), 40);
    assert_eq!(*result.get("r_min").unwrap(), 10);
    assert_eq!(*result.get("g_max").unwrap(), 50);
    assert_eq!(*result.get("g_min").unwrap(), 20);
    assert_eq!(*result.get("b_max").unwrap(), 60);
    assert_eq!(*result.get("b_min").unwrap(), 30);
    assert!(((*result.get("r_dvalue").unwrap() as f64 - 10.0).abs()) < 1e-6);
    assert!(((*result.get("g_dvalue").unwrap() as f64 - 10.0).abs()) < 1e-6);
    assert!(((*result.get("b_dvalue").unwrap() as f64 - 10.0).abs()) < 1e-6);
}

#[test]
fn test_group_by_accuracy_edge() {
    let colors = vec![(2, (10, 20, 30)), (1, (11, 21, 31))];
    let grouped = alg::group_by_accuracy(&colors, 1);
    let mut found = 0;
    for i in 0..grouped.len() {
        for j in 0..grouped[i].len() {
            for k in 0..grouped[i][j].len() {
                found += grouped[i][j][k].len();
            }
        }
    }
    assert_eq!(found, 2);
}

#[test]
fn test_group_by_accuracy_large_range() {
    let colors = vec![(1, (0, 0, 0)), (1, (127, 127, 127)), (1, (255, 255, 255))];
    let grouped = alg::group_by_accuracy(&colors, 3);
    let mut out = vec![];
    for i in 0..3 {
        for j in 0..3 {
            for k in 0..3 {
                for val in &grouped[i][j][k] {
                    out.push(*val);
                }
            }
        }
    }
    assert_eq!(out.len(), 3);
}

#[test]
fn test_get_weighted_mean_weighted() {
    let group = vec![(10, (100, 150, 200)), (10, (110, 130, 170))];
    let weighted = alg::get_weighted_mean(&group);
    assert_eq!(weighted.0, 20);
    assert_eq!(weighted.1.0, 105);
    assert_eq!(weighted.1.1, 140);
    assert_eq!(weighted.1.2, 185);
}

#[test]
fn test_get_weighted_mean_single() {
    let group = vec![(1, (1, 2, 3))];
    let weighted = alg::get_weighted_mean(&group);
    assert_eq!(weighted, (1, (1, 2, 3)));
}

#[test]
fn test_group_by_accuracy_all_same_color() {
    let colors = vec![(2, (10, 20, 30)), (2, (10, 20, 30))];
    let grouped = alg::group_by_accuracy(&colors, 3);
    let mut found = 0;
    for i in 0..3 {
        for j in 0..3 {
            for k in 0..3 {
                found += grouped[i][j][k].len();
            }
        }
    }
    assert_eq!(found, 2);
}