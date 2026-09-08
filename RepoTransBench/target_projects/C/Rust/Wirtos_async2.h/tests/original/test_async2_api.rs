use async2::{AsyncArr, async_new, async_resume, async_free};

#[test]
fn test_async_memory() {
    let state = async_new();
    assert!(state != std::ptr::null_mut());
    async_resume(state);
    async_resume(state);
    async_free(state);
}

#[test]
fn test_async_nullptrs() {
    // Test NULL pointer handling for all public API
    async_free(std::ptr::null_mut());
    async_resume(std::ptr::null_mut());

    // In Rust, we can't test null pointers directly as in C
    // This is handled by the Option type in a real implementation
}

#[test]
fn test_async_arr() {
    let mut arr = AsyncArr {
        count: 0,
        values: [0; 10],
    };
    
    arr.init();
    let x = 42;
    assert_eq!(arr.push(x), 1);
    assert_eq!(arr.push(x + 1), 1);
    assert_eq!(arr.push(x + 2), 1);

    let count = arr.count;
    for i in count..10 {
        assert!(arr.push(i));
    }
    // Buffer full now
    assert_eq!(arr.push(100), 0);

    let top = arr.pop();
    assert!(top >= 0);

    // Test splice normal case
    arr.splice(0, 1);

    // Test splice edge cases (negative, past end, zero)
    arr.splice(-1, 2);  // should do nothing
    arr.splice(arr.count, 1); // should do nothing
    arr.splice(0, 0); // should do nothing
    arr.splice(0, 100); // trim to count

    arr.destroy();
}

#[test]
fn test_async_pop_empty() {
    let mut arr = AsyncArr {
        count: 0,
        values: [0; 10],
    };
    
    arr.init();
    assert_eq!(arr.pop(), -1);
}