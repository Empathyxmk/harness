use sedgewick_algorithms_exercises::array_sorts::shell_sort;

#[test]
fn test_shell_sort_public() {
    // Varied positive/negative
    let mut arr = [37, -12, 49, 0, 27, 100, -57, 4];
    let expected = [-57, -12, 0, 4, 27, 37, 49, 100];
    shell_sort(&mut arr);
    assert_eq!(arr, expected);

    // Two elements swapped
    let mut arr = [2, 1];
    let expected = [1, 2];
    shell_sort(&mut arr);
    assert_eq!(arr, expected);

    // Single
    let mut arr = [-88];
    shell_sort(&mut arr);
    assert_eq!(arr, [-88]);

    // Large mostly reversed
    let mut arr = [81, 70, 43, 32, 25, 17, 13, 3];
    let expected = [3, 13, 17, 25, 32, 43, 70, 81];
    shell_sort(&mut arr);
    assert_eq!(arr, expected);

    // With zeros & duplicates
    let mut arr = [0, 2, 2, 0, 1, 0];
    let expected = [0, 0, 0, 1, 2, 2];
    shell_sort(&mut arr);
    assert_eq!(arr, expected);

    // Already sorted
    let mut arr = [3, 7, 14, 89];
    let expected = [3, 7, 14, 89];
    shell_sort(&mut arr);
    assert_eq!(arr, expected);
}