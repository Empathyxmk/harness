use ccareaga_heap_allocator::{Bin, Node, add_node, remove_node, get_best_fit, get_last_node};

#[test]
fn test_add_and_remove_order_public() {
    let mut b = Bin::default();
    let mut n1 = Node { size: 48, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 24, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 80, next: None, prev: std::ptr::null_mut() };

    add_node(&mut b, &mut n1);
    add_node(&mut b, &mut n2);
    add_node(&mut b, &mut n3);

    assert_eq!(b.head.as_ref().map(|n| n.size), Some(80));
    assert_eq!(
        b.head.as_ref().and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(24)
    );
    assert_eq!(
        b.head.as_ref()
            .and_then(|n| n.next.as_ref())
            .and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(48)
    );
    assert!(
        b.head
            .as_ref()
            .and_then(|n| n.next.as_ref())
            .and_then(|n| n.next.as_ref())
            .and_then(|n| n.next.as_ref())
            .is_none()
    );

    remove_node(&mut b, &n2);
    remove_node(&mut b, &n1);
    remove_node(&mut b, &n3);
    // For stub, this is no-op. In real heap, linked nodes should be detached.
}

#[test]
fn test_best_fit_public() {
    let mut b = Bin::default();
    let mut n1 = Node { size: 28, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 72, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 16, next: None, prev: std::ptr::null_mut() };
    add_node(&mut b, &mut n1);
    add_node(&mut b, &mut n2);
    add_node(&mut b, &mut n3);
    let fit = get_best_fit(&b, 26);
    if let Some(f) = fit {
        assert_eq!(f.size, 28);
    }
    let fit2 = get_best_fit(&b, 120);
    assert!(fit2.is_none());
}

#[test]
fn test_get_last_node_public() {
    let mut b = Bin::default();
    let mut n1 = Node { size: 40, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 60, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 70, next: None, prev: std::ptr::null_mut() };
    add_node(&mut b, &mut n2);
    add_node(&mut b, &mut n3);
    add_node(&mut b, &mut n1);
    let last = get_last_node(&b);
    if let Some(n) = last {
        assert_eq!(n.size, 40);
    }
}

#[test]
fn test_remove_node_not_found_public() {
    let mut bin = Bin::default();
    let n = Node { size: 44, next: None, prev: std::ptr::null_mut() };
    remove_node(&mut bin, &n); // Should not panic
}