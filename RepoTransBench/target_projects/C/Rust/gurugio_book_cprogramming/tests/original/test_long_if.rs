use gurugio::very_long_if;

#[test]
fn test_long_if_all_positive() {
    assert_eq!(very_long_if(1, 2, 3), 1);
}

#[test]
fn test_long_if_all_negative() {
    assert_eq!(very_long_if(-1, -2, -3), -1);
}

#[test]
fn test_long_if_zeros() {
    assert_eq!(very_long_if(0, 1, 2), 0);
}

#[test]
fn test_long_if_catch_rest() {
    assert_eq!(very_long_if(1, -2, 3), 99);
}