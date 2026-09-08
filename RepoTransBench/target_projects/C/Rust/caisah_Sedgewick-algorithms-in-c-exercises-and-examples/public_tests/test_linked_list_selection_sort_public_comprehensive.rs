use sedgewick_algorithms_exercises::linked_list_selection_sort::{Node, selection_sort};

fn init_public(arr: &[i32]) -> Option<Box<Node>> {
    Node::from_vec(arr)
}

fn expect_sort(input: &[i32], expected: &[i32]) {
    let h = init_public(input);
    let s = selection_sort(h);
    let mut sopt = s.as_ref();
    for (i, &exp) in expected.iter().enumerate() {
        if let Some(node) = sopt {
            assert_eq!(node.item, exp, "[FAIL] Sorting result mismatch at {i}: expected {exp} got {}", node.item);
            sopt = node.next.as_ref();
        } else {
            panic!("[FAIL] List too short at {i}!");
        }
    }
    if sopt.is_some() {
        panic!("[FAIL] List too long!");
    }
}

#[test]
fn public_linked_list_selection_sort_batch() {
    // Test 1: descending
    let a1 = [123, 97, 44, 32, 31];
    let e1 = [31, 32, 44, 97, 123];
    expect_sort(&a1, &e1);

    // Test 2: ascending
    let a2 = [1, 2, 3, 4, 5];
    let e2 = [1, 2, 3, 4, 5];
    expect_sort(&a2, &e2);

    // Test 3: single item (edge)
    let a3 = [999];
    let e3 = [999];
    expect_sort(&a3, &e3);

    // Test 4: duplicates
    let a4 = [13, 13, 7, 7, 21];
    let e4 = [7, 7, 13, 13, 21];
    expect_sort(&a4, &e4);

    // Test 5: mix
    let a5 = [42, 17, 50, 17, 5, 23];
    let e5 = [5, 17, 17, 23, 42, 50];
    expect_sort(&a5, &e5);
}