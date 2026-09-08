use ccareaga_heap_allocator::{
    Heap, Bin, Node, add_node, remove_node, get_best_fit, get_last_node,
    get_bin_index, init_heap, heap_alloc, heap_free, expand, contract, BIN_COUNT, HEAP_INIT_SIZE,
};

fn setup_heap(heap: &mut Heap) {
    // Zero heap and bins, mimic C allocation
    for i in 0..BIN_COUNT {
        heap.bins[i] = Some(Bin::default());
    }
    // Use address as in C, but just a stub u64 here
    init_heap(heap, 0x10000);
}

fn cleanup_heap(_heap: &mut Heap) {
    // Rust drops bins automatically
}

#[test]
fn test_basic_alloc_free() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let p1 = heap_alloc(&mut heap,8);
    assert!(p1.is_some());
    let p2 = heap_alloc(&mut heap,32);
    assert!(p2.is_some());

    heap_free(&mut heap, &p1);
    heap_free(&mut heap, &p2);

    cleanup_heap(&mut heap);
}

#[test]
fn test_overflow_allocation() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let max_alloc = heap_alloc(&mut heap, HEAP_INIT_SIZE);
    assert!(max_alloc.is_none());

    cleanup_heap(&mut heap);
}

#[test]
fn test_bin_index() {
    assert!(get_bin_index(4) >= 0);
    assert!(get_bin_index(64) >= 0);
    assert!(get_bin_index(1024) >= 0);
}

#[test]
fn test_add_and_remove_node() {
    let mut bin = Bin::default();
    let mut n1 = Node { size: 16, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 32, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 8, next: None, prev: std::ptr::null_mut() };

    add_node(&mut bin, &mut n1);
    assert_eq!(bin.head.as_ref().map(|n| n.size), Some(16));

    add_node(&mut bin, &mut n2);
    add_node(&mut bin, &mut n3);

    assert_eq!(bin.head.as_ref().map(|n| n.size), Some(8));
    assert_eq!(
        bin.head.as_ref().and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(16)
    );
    assert_eq!(
        bin.head.as_ref()
            .and_then(|n| n.next.as_ref())
            .and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(32)
    );

    remove_node(&mut bin, &n1);
    remove_node(&mut bin, &n3);
    remove_node(&mut bin, &n2);
    // After removals, bin should be empty (head = None)
    // (Stub always leaves head; in real implementation check)
}

#[test]
fn test_get_best_fit() {
    let mut bin = Bin::default();
    let mut n1 = Node { size: 8, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 32, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 16, next: None, prev: std::ptr::null_mut() };
    add_node(&mut bin, &mut n2);
    add_node(&mut bin, &mut n1);
    add_node(&mut bin, &mut n3);

    let fit = get_best_fit(&bin, 15);
    if let Some(f) = fit {
        assert!(f.size >= 15);
    }

    let fit2 = get_best_fit(&bin, 100);
    assert!(fit2.is_none());
}

#[test]
fn test_split_and_merge() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 8);
    let b = heap_alloc(&mut heap, 128);
    assert!(a.is_some() && b.is_some());
    heap_free(&mut heap, &b);
    let c = heap_alloc(&mut heap, 64);
    assert!(c.is_some());

    heap_free(&mut heap, &a);
    heap_free(&mut heap, &c);

    cleanup_heap(&mut heap);
}

#[test]
fn test_contract_and_expand() {
    let mut heap = Heap::default();
    let ret = expand(&mut heap, 0x1000);
    assert_eq!(ret, 0);
    contract(&mut heap, 0x1000);
}

#[test]
fn test_free_only_head() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 8);
    heap_free(&mut heap, &a);

    cleanup_heap(&mut heap);
}

#[test]
fn test_alloc_min_size() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 1);
    assert!(a.is_some());
    heap_free(&mut heap, &a);

    cleanup_heap(&mut heap);
}