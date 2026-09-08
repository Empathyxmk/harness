// Translated from C: tests/test_example_public.c

#[allow(dead_code)]
fn example_add(a: i32, b: i32) -> i32 {
    a + b
}

#[allow(dead_code)]
fn example_mul(a: i32, b: i32) -> i32 {
    a * b
}

#[test]
fn test_example_add() {
    // ADD tests with new input
    assert_eq!(example_add(3, 7), 10);
    assert_eq!(example_add(-5, 10), 5);
}

#[test]
fn test_example_mul() {
    // MUL tests with new input
    assert_eq!(example_mul(2, 5), 10);
    assert_eq!(example_mul(-4, 8), -32);
}