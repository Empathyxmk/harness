use true_random::true_random;

#[test]
fn test_true_random_output() {
    // Just ensure the function can be called 15 times without crashing
    for _ in 0..15 {
        let random_value = true_random();
        let _ = random_value; // Use the variable to avoid compiler warnings
    }
}