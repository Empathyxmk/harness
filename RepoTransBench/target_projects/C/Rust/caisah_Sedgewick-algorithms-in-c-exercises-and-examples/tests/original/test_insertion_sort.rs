use sedgewick_algorithms_exercises::array_sorts::insertion_sort;

#[test]
fn test_random() {
    let mut a = [5, 2, 9, 3, 1];
    let expected = [1, 2, 3, 5, 9];
    insertion_sort(&mut a);
    assert_eq!(a, expected);
}

#[test]
fn test_sorted() {
    let mut a = [1, 2, 3, 4];
    let expected = [1, 2, 3, 4];
    insertion_sort(&mut a);
    assert_eq!(a, expected);
}

#[test]
fn test_reverse() {
    let mut a = [4, 3, 2, 1];
    let expected = [1, 2, 3, 4];
    insertion_sort(&mut a);
    assert_eq!(a, expected);
}

#[test]
fn test_equal() {
    let mut a = [2, 2, 2];
    let expected = [2, 2, 2];
    insertion_sort(&mut a);
    assert_eq!(a, expected);
}

#[test]
fn test_single() {
    let mut a = [42];
    let expected = [42];
    insertion_sort(&mut a);
    assert_eq!(a, expected);
}