use async2::AsyncArr;

#[test]
fn public_test_async2_api() {
    let mut arr = AsyncArr {
        count: 0,
        values: [0; 10],
    };

    // Push different numbers than private (e.g., 5, 16, 25)
    arr.push(5);
    arr.push(16);
    arr.push(25);

    assert_eq!(arr.count, 3);
    assert_eq!(arr.values[0], 5);
    assert_eq!(arr.values[1], 16);
    assert_eq!(arr.values[2], 25);

    // Splice at a different index (remove second element)
    arr.splice(1, 1);

    assert_eq!(arr.count, 2);
    assert_eq!(arr.values[0], 5);
    assert_eq!(arr.values[1], 25);

    // Further splice (remove first element)
    arr.splice(0, 1);
    assert_eq!(arr.count, 1);
    assert_eq!(arr.values[0], 25);

    // Test destroy resets to zero
    arr.destroy();
    assert_eq!(arr.count, 0);
}