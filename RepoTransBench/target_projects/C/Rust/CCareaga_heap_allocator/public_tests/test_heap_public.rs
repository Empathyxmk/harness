use ccareaga_heap_allocator::{
    Heap, Bin, Node, add_node, remove_node, get_best_fit, get_last_node,
    get_bin_index, init_heap, heap_alloc, heap_free, expand, contract, BIN_COUNT, HEAP_INIT_SIZE,
};

fn setup_heap(heap: &mut Heap) {
    for i in 0..BIN_COUNT {
        heap.bins[i] = Some(Bin::default());
    }
    init_heap(heap, 0x20000);
}

fn cleanup_heap(_heap: &mut Heap) {}

#[test]
fn test_basic_alloc_free_public() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let p1 = heap_alloc(&mut heap, 16);
    assert!(p1.is_some());
    let p2 = heap_alloc(&mut heap, 64);
    assert!(p2.is_some());

    heap_free(&mut heap, &p2);
    heap_free(&mut heap, &p1);

    cleanup_heap(&mut heap);
}

#[test]
fn test_overflow_allocation_public() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let large_alloc = heap_alloc(&mut heap, HEAP_INIT_SIZE * 2);
    assert!(large_alloc.is_none());

    cleanup_heap(&mut heap);
}

#[test]
fn test_bin_index_public() {
    assert!(get_bin_index(12) >= 0);
    assert!(get_bin_index(88) >= 0);
    assert!(get_bin_index(2048) >= 0);
}

#[test]
fn test_add_and_remove_node_public() {
    let mut bin = Bin::default();
    let mut n1 = Node { size: 24, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 48, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 12, next: None, prev: std::ptr::null_mut() };

    add_node(&mut bin, &mut n2);
    assert_eq!(bin.head.as_ref().map(|n| n.size), Some(48));

    add_node(&mut bin, &mut n1);
    add_node(&mut bin, &mut n3);

    assert_eq!(bin.head.as_ref().map(|n| n.size), Some(12));
    assert_eq!(
        bin.head.as_ref().and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(24)
    );
    assert_eq!(
        bin.head.as_ref()
            .and_then(|n| n.next.as_ref())
            .and_then(|n| n.next.as_ref().map(|n| n.size)),
        Some(48)
    );

    remove_node(&mut bin, &n1);
    remove_node(&mut bin, &n3);
    remove_node(&mut bin, &n2);
}

#[test]
fn test_get_best_fit_public() {
    let mut bin = Bin::default();
    let mut n1 = Node { size: 12, next: None, prev: std::ptr::null_mut() };
    let mut n2 = Node { size: 64, next: None, prev: std::ptr::null_mut() };
    let mut n3 = Node { size: 24, next: None, prev: std::ptr::null_mut() };
    add_node(&mut bin, &mut n2);
    add_node(&mut bin, &mut n1);
    add_node(&mut bin, &mut n3);

    let fit = get_best_fit(&bin, 20);
    if let Some(f) = fit {
        assert!(f.size >= 20);
    }

    let fit2 = get_best_fit(&bin, 128);
    assert!(fit2.is_none());
}

#[test]
fn test_split_and_merge_public() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 16);
    let b = heap_alloc(&mut heap, 256);
    assert!(a.is_some() && b.is_some());
    heap_free(&mut heap, &a);
    let c = heap_alloc(&mut heap, 128);
    assert!(c.is_some());

    heap_free(&mut heap, &b);
    heap_free(&mut heap, &c);

    cleanup_heap(&mut heap);
}

#[test]
fn test_contract_and_expand_public() {
    let mut heap = Heap::default();
    let ret = expand(&mut heap, 0x2000);
    assert_eq!(ret, 0);
    contract(&mut heap, 0x2000);
}

#[test]
fn test_free_only_head_public() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 16);
    heap_free(&mut heap, &a);

    cleanup_heap(&mut heap);
}

#[test]
fn test_alloc_min_size_public() {
    let mut heap = Heap::default();
    setup_heap(&mut heap);

    let a = heap_alloc(&mut heap, 2);
    assert!(a.is_some());
    heap_free(&mut heap, &a);

    cleanup_heap(&mut heap);
}