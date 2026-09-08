use sedgewick_algorithms_exercises::array_sorts::shell_sort;

fn check(a: &[i32], b: &[i32]) -> bool {
    a == b
}

#[test]
fn test_shell_basic() {
    let mut a = [14, 2, 6, 4, 11, 7];
    let expected = [2, 4, 6, 7, 11, 14];
    shell_sort(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_shell_sorted() {
    let mut a = [1, 2, 3, 4, 5];
    let expected = [1, 2, 3, 4, 5];
    shell_sort(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_shell_reverse() {
    let mut a = [8, 6, 4, 2];
    let expected = [2, 4, 6, 8];
    shell_sort(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_shell_equal() {
    let mut a = [9, 9, 9];
    let expected = [9, 9, 9];
    shell_sort(&mut a);
    assert!(check(&a, &expected));
}