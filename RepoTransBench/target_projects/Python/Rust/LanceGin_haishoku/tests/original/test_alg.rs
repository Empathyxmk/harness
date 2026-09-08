use haishoku_rs::alg;

fn get_colors_tuple() -> Vec<(usize, (u8, u8, u8))> {
    vec![
        (10, (100, 150, 200)),
        (5, (120, 130, 140)),
        (8, (110, 170, 130)),
        (15, (90, 80, 210)),
        (3, (180, 50, 60)),
        (2, (240, 10, 20)),
    ]
}

#[test]
fn test_sort_by_rgb() {
    let colors = get_colors_tuple();
    let result = alg::sort_by_rgb(&colors);
    let mut expected = colors.clone();
    expected.sort_by_key(|x| x.1);
    assert_eq!(result, expected);
}

#[test]
fn test_rgb_maximum() {
    let colors = get_colors_tuple();
    let result = alg::rgb_maximum(&colors);
    assert_eq!(*result.get("r_max").unwrap(), 240);
    assert_eq!(*result.get("r_min").unwrap(), 90);
    assert_eq!(*result.get("g_max").unwrap(), 170);
    assert_eq!(*result.get("g_min").unwrap(), 10);
    assert_eq!(*result.get("b_max").unwrap(), 210);
    assert_eq!(*result.get("b_min").unwrap(), 20);
    assert_eq!(result.len(), 9);
}

#[test]
fn test_group_by_accuracy() {
    let colors = get_colors_tuple();
    let sorted_tuple = alg::sort_by_rgb(&colors);
    let rgb = alg::group_by_accuracy(&sorted_tuple, 3);
    assert_eq!(rgb.len(), 3);
    assert_eq!(rgb[0].len(), 3);
    assert_eq!(rgb[0][0].len(), 3);
}

#[test]
fn test_get_weighted_mean() {
    let group = vec![(10, (100, 150, 200)), (5, (120, 130, 140))];
    let w_mean = alg::get_weighted_mean(&group);
    assert_eq!(w_mean.0, 15);
    assert_eq!(w_mean.1 .0, ((100*10+120*5)/15) as u8);
    assert_eq!(w_mean.1 .1, ((150*10+130*5)/15) as u8);
    assert_eq!(w_mean.1 .2, ((200*10+140*5)/15) as u8);
}

#[test]
fn test_get_weighted_mean_single() {
    let group = vec![(7, (50, 60, 70))];
    let w_mean = alg::get_weighted_mean(&group);
    assert_eq!(w_mean, (7, (50, 60, 70)));
}

#[test]
#[should_panic(expected = "Total weight is zero")]
fn test_get_weighted_mean_zero() {
    alg::get_weighted_mean(&[]);
}