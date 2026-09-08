use sedgewick_algorithms_exercises::array_sorts::{bubble_sort, bubble_sort_improved};

fn check(a: &[i32], b: &[i32]) -> bool {
    a == b
}

#[test]
fn test_bubble_basic() {
    let mut a = [5, 4, 3, 2, 1, 0];
    let expected = [0, 1, 2, 3, 4, 5];
    bubble_sort(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_bubble_already_sorted() {
    let mut a = [1, 2, 3, 4, 5];
    let expected = [1, 2, 3, 4, 5];
    bubble_sort(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_bubble_improved_basic() {
    let mut a = [5, 4, 3, 2, 1, 0];
    let expected = [0, 1, 2, 3, 4, 5];
    bubble_sort_improved(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_bubble_improved_already_sorted() {
    let mut a = [1, 2, 3, 4, 5];
    let expected = [1, 2, 3, 4, 5];
    bubble_sort_improved(&mut a);
    assert!(check(&a, &expected));
}

#[test]
fn test_bubble_duplicates() {
    let mut a = [2, 3, 3, 1, 2, 0];
    let expected = [0, 1, 2, 2, 3, 3];
    bubble_sort(&mut a);
    assert!(check(&a, &expected));
}