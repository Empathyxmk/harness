use jwasham_practice_c_rust::quick_sort::{is_sorted, contain_same_ints};

#[test]
fn test_is_sorted_success() {
    let arr = [1, 2, 3, 4, 5];
    assert!(is_sorted(&arr));
}

#[test]
fn test_is_sorted_fail() {
    let arr = [1, 2, 3, 2, 5];
    assert!(!is_sorted(&arr));
}

#[test]
fn test_contain_same_ints_true() {
    let arr1 = [1, 2, 2, 3];
    let arr2 = [3, 2, 1, 2];
    assert!(contain_same_ints(&arr1, &arr2));
}

#[test]
fn test_contain_same_ints_false() {
    let arr1 = [1, 2, 3, 4];
    let arr2 = [1, 2, 3, 5];
    assert!(!contain_same_ints(&arr1, &arr2));
}