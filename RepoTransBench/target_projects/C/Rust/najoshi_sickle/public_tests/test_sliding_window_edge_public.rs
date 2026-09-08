use najoshi_sickle::sliding::sliding_window_arr;

#[test]
fn test_sliding_window_edge_public() {
    let arr1 = [40, 41, 39, 45, 44];
    assert_eq!(sliding_window_arr(&arr1, 5, 3), 41);

    let arr2 = [33, 33, 33, 33];
    assert_eq!(sliding_window_arr(&arr2, 4, 2), 33);

    let arr3 = [100, 101, 102, 103, 104];
    assert_eq!(sliding_window_arr(&arr3, 5, 5), 102);

    let arr4 = [10, 20, 30];
    assert_eq!(sliding_window_arr(&arr4, 3, 2), 20);

    let arr5 = [55, 56, 57, 58, 59, 60];
    assert_eq!(sliding_window_arr(&arr5, 6, 1), 57);
}