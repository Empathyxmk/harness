use glb_director::*;

#[test]
fn test_add() {
    // Basic, zero, negative and positive test cases
    assert_eq!(add(1, 2), 3);
    assert_eq!(add(-4, 4), 0);
    assert_eq!(add(-7, -5), -12);
    assert_eq!(add(100, 50), 150);
}

#[test]
fn test_is_palindrome() {
    // Palindromes and non-palindromes
    assert_eq!(is_palindrome("madam"), 1);
    assert_eq!(is_palindrome("racecar"), 1);
    assert_eq!(is_palindrome("hello"), 0);
    assert_eq!(is_palindrome("step on no pets"), 1);
    assert_eq!(is_palindrome("abc"), 0);
    assert_eq!(is_palindrome(""), 1); // edge, empty string is palindrome
    assert_eq!(is_palindrome("a"), 1); // single character is palindrome
}

#[test]
fn test_sign() {
    assert_eq!(sign(10), 1);
    assert_eq!(sign(-20), -1);
    assert_eq!(sign(0), 0);
    assert_eq!(sign(12345), 1);
    assert_eq!(sign(-1), -1);
}