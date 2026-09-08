use sedgewick_algorithms_exercises::array_sorts::bubble_sort;

#[test]
fn test_bubble_sort_public() {
    // All unique random
    let mut arr = [21, 17, -8, 3, 5];
    let expected = [-8, 3, 5, 17, 21];
    bubble_sort(&mut arr);
    assert_eq!(arr, expected);

    // array with duplicates
    let mut arr = [10, 10, 5, 7, 5];
    let expected = [5, 5, 7, 10, 10];
    bubble_sort(&mut arr);
    assert_eq!(arr, expected);

    // Already sorted
    let mut arr = [1, 2, 3, 4];
    let expected = [1, 2, 3, 4];
    bubble_sort(&mut arr);
    assert_eq!(arr, expected);

    // Two elements, reverse
    let mut arr = [9, 2];
    bubble_sort(&mut arr);
    assert_eq!(arr, [2, 9]);

    // One element
    let mut arr = [-1234];
    bubble_sort(&mut arr);
    assert_eq!(arr, [-1234]);

    // Zeros and negative
    let mut arr = [0, 0, 0, 0, 0, -1];
    let expected = [-1, 0, 0, 0, 0, 0];
    bubble_sort(&mut arr);
    assert_eq!(arr, expected);
}