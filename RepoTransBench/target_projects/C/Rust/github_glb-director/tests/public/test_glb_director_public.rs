use glb_director::*;

#[test]
fn test_sum_public() {
    assert_eq!(sum(3, 11), 14);
    assert_eq!(sum(-2, 7), 5);
    assert_eq!(sum(44, 77), 121);
    assert_eq!(sum(-8, -12), -20);
}

#[test]
fn test_is_palindrome_public() {
    assert_eq!(is_palindrome("evil olive"), 1);
    assert_eq!(is_palindrome("civic"), 1);
    assert_eq!(is_palindrome("palindrome"), 0);
    assert_eq!(is_palindrome("openai"), 0);
}

#[test]
fn test_max_of_three_public() {
    assert_eq!(max_of_three(4, 2, 5), 5);
    assert_eq!(max_of_three(-5, -9, -2), -2);
    assert_eq!(max_of_three(15, 32, 25), 32);
    assert_eq!(max_of_three(77, 77, 77), 77);
}

#[test]
fn test_average_public() {
    let arr1 = [2.0, 4.0, 6.0];
    assert_eq!(average(&arr1, 3), 4.0);

    let arr2 = [9.5, 3.5];
    assert_eq!(average(&arr2, 2), 6.5);

    let arr3 = [12.0];
    assert_eq!(average(&arr3, 1), 12.0);

    let arr4 = [-12.0, -8.0, -16.0, -4.0];
    assert_eq!(average(&arr4, 4), -10.0);
}

#[test]
fn test_factorial_public() {
    assert_eq!(factorial(1), 1);
    assert_eq!(factorial(4), 24);
    assert_eq!(factorial(7), 5040);
    assert_eq!(factorial(2), 2);
}