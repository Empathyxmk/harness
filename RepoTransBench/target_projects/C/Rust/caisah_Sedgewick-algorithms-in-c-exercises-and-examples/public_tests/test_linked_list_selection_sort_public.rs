use sedgewick_algorithms_exercises::linked_list_selection_sort::{Node, selection_sort};

// Helper function to convert Vec<i32> to linked list
fn push(head: Option<Box<Node>>, v: i32) -> Option<Box<Node>> {
    Some(Box::new(Node { item: v, next: head }))
}

fn list_to_vec(head: &Option<Box<Node>>, maxlen: usize) -> Vec<i32> {
    let mut arr = Vec::with_capacity(maxlen);
    let mut cur = head;
    for _ in 0..maxlen {
        if let Some(node) = cur {
            arr.push(node.item);
            cur = &node.next;
        } else {
            break;
        }
    }
    arr
}

#[test]
fn test_list_selection_sort_various() {
    // test with negative and positive
    let a = [21, -4, 15, 9, 0, -13, 48, 7];
    let expected = [-13, -4, 0, 7, 9, 15, 21, 48];
    let mut h: Option<Box<Node>> = None;
    for &v in a.iter().rev() {
        h = push(h, v);
    }
    let h = selection_sort(h);
    let out = list_to_vec(&h, 8);
    assert_eq!(out, expected);

    // test length 1
    let h = push(None, 42);
    let h = selection_sort(h);
    assert!(h.is_some() && h.as_ref().unwrap().item == 42 && h.as_ref().unwrap().next.is_none());

    // test with duplicates
    let a = [8, 8, 2, 2, 5, 5];
    let expected = [2, 2, 5, 5, 8, 8];
    let mut h: Option<Box<Node>> = None;
    for &v in a.iter().rev() {
        h = push(h, v);
    }
    let h = selection_sort(h);
    let out = list_to_vec(&h, 6);
    assert_eq!(out, expected);

    // test generic order
    let a = [11, 76, 34, 67, 54, 19];
    let expected = [11, 19, 34, 54, 67, 76];
    let mut h: Option<Box<Node>> = None;
    for &v in a.iter().rev() {
        h = push(h, v);
    }
    let h = selection_sort(h);
    let out = list_to_vec(&h, 6);
    assert_eq!(out, expected);

    // test empty
    let h: Option<Box<Node>> = None;
    let h = selection_sort(h);
    assert!(h.is_none());
}