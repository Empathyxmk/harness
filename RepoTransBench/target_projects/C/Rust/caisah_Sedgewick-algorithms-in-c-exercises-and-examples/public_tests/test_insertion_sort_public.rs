use sedgewick_algorithms_exercises::array_sorts::insertion_sort;

#[test]
fn test_insertion_sort_public() {
    // All negative and positive
    let mut arr = [12, -9, 0, 42, -3, 25];
    let expected = [-9, -3, 0, 12, 25, 42];
    insertion_sort(&mut arr);
    assert_eq!(arr, expected);

    // Reverse-sorted array
    let mut arr = [7, 6, 5, 4, 3, 2, 1];
    let expected = [1, 2, 3, 4, 5, 6, 7];
    insertion_sort(&mut arr);
    assert_eq!(arr, expected);

    // With duplicates and large
    let mut arr = [99, -8, -8, 0, 1, 44, 44, 3];
    let expected = [-8, -8, 0, 1, 3, 44, 44, 99];
    insertion_sort(&mut arr);
    assert_eq!(arr, expected);

    // Already sorted
    let mut arr = [2, 4, 8, 16, 32];
    let expected = [2, 4, 8, 16, 32];
    insertion_sort(&mut arr);
    assert_eq!(arr, expected);

    // Single, zero/empty
    let mut arr = [11];
    insertion_sort(&mut arr);
    assert_eq!(arr, [11]);

    // all same
    let mut arr = [5, 5, 5, 5];
    insertion_sort(&mut arr);
    assert_eq!(arr, [5, 5, 5, 5]);

    // descending with negatives
    let mut arr = [10, 0, -5, -12];
    let expected = [-12, -5, 0, 10];
    insertion_sort(&mut arr);
    assert_eq!(arr, expected);
}