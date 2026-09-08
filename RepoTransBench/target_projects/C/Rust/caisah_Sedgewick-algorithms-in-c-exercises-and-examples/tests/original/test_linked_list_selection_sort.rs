use sedgewick_algorithms_exercises::linked_list_selection_sort::{Node, selection_sort};

fn create_list(vals: &[i32]) -> Option<Box<Node>> {
    Node::from_vec(vals)
}

fn list_is_sorted(h: &Option<Box<Node>>) -> bool {
    Node::is_sorted(h)
}

#[test]
fn test_sort_basic() {
    let vals = [5, 1, 3, 7];
    let head = create_list(&vals);
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}

#[test]
fn test_sort_sorted() {
    let vals = [1, 2, 3, 4];
    let head = create_list(&vals);
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}

#[test]
fn test_sort_reverse() {
    let vals = [4, 3, 2, 1];
    let head = create_list(&vals);
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}

#[test]
fn test_sort_equal() {
    let vals = [2, 2, 2];
    let head = create_list(&vals);
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}

#[test]
fn test_sort_single() {
    let vals = [100];
    let head = create_list(&vals);
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}

#[test]
fn test_sort_empty() {
    let head: Option<Box<Node>> = None;
    let sorted = selection_sort(head);
    assert!(list_is_sorted(&sorted));
}