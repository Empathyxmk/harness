use nickjj_ansible_docker::dummy_logic::*;

#[test]
fn test_increment_public() {
    assert_eq!(increment(10), 11);
    assert_eq!(increment(-4), -3);
}

#[test]
fn test_sum_public() {
    assert_eq!(total(&[3, 8, 12]), 23);
    assert_eq!(total(&[]), 0);
    assert_eq!(total(&[-2, 5]), 3);
}

#[test]
fn test_is_even_public() {
    assert!(is_even(100));
    assert!(!is_even(15));
    assert!(is_even(-22));
}

#[test]
fn test_custom_case_public() {
    let numbers = [6, 7, 8, 9];
    let even_count = numbers.iter().filter(|&&n| is_even(n)).count();
    assert_eq!(even_count, 2);
}

#[test]
fn test_zero_increment_public() {
    assert_eq!(increment(0), 1);
}

#[test]
fn test_negative_total_public() {
    assert_eq!(total(&[-5, -5, -10]), -20);
}