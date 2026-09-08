use async2::AsyncArr;

#[test]
fn test_async_arr_splice_negative_count() {
    let mut arr = AsyncArr {
        count: 0,
        values: [0; 10],
    };
    
    arr.init();

    // Fill some data
    for i in 0..5 {
        assert_eq!(arr.push(i), 1);
    }
    
    // Use splice with maximum len, should not underflow
    arr.splice(0, 100);
    assert_eq!(arr.count, 0);

    // force count, then splice
    arr.count = 2;
    arr.values[0] = 10;
    arr.values[1] = 11;
    arr.splice(1, 2);  // only one left, should just remove that one
    assert_eq!(arr.count, 1);
    assert_eq!(arr.values[0], 10);

    arr.count = 0;
    arr.splice(0, 1); // nothing to remove, should stay at zero
    assert_eq!(arr.count, 0);
}

#[test]
fn test_async_arr_destroy_resets_count() {
    let mut arr = AsyncArr {
        count: 5,
        values: [0; 10],
    };
    
    arr.destroy();
    assert_eq!(arr.count, 0);
    
    // Destroying again is safe
    arr.destroy();
    assert_eq!(arr.count, 0);
}