use async2::AsyncArr;

#[test]
fn public_test_async2_arr_edgecases() {
    let mut arr = AsyncArr {
        count: 0,
        values: [0; 10],
    };

    // Test pushing then splicing all
    arr.push(100);
    arr.push(200);

    // Edge: remove whole array in one go
    arr.splice(0, 2);
    assert_eq!(arr.count, 0);

    // Edge: try splicing more than count (should not crash or go negative)
    arr.push(44);
    arr.splice(0, 5);
    assert_eq!(arr.count, 0);

    // Edge: try splicing from index greater than count (should not crash)
    arr.push(77);
    arr.splice(5, 1); // out of range
    assert_eq!(arr.count, 1);
    assert_eq!(arr.values[0], 77);

    // Test destroy resets to zero
    arr.destroy();
    assert_eq!(arr.count, 0);
}