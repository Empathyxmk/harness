//! Additional, more comprehensive tests for pool (translated from test_ext.c)

use jobtalle_pool::*;
use std::ptr;
use std::mem;

const DUMMY_BLOCK_SIZE: usize = 2;

// Helper struct for testing, modeling a freed node pointer in pool (from C)
#[repr(C)]
struct PoolFreed {
    next: *mut PoolFreed,
}

/// Helper to allocate a block of memory for custom testing for memory pool structures
unsafe fn alloc_pool_freed() -> *mut PoolFreed {
    let layout = std::alloc::Layout::new::<PoolFreed>();
    std::alloc::alloc(layout) as *mut PoolFreed
}

#[test]
fn test_pool_initialize_edge_cases() {
    // element_size < sizeof(poolFreed)
    let mut p = Pool::default();
    pool_initialize(&mut p, 1, DUMMY_BLOCK_SIZE).unwrap();
    assert!(p.element_size >= mem::size_of::<PoolFreed>());
    pool_free_pool(&mut p);

    // element_size == sizeof(poolFreed)
    pool_initialize(&mut p, mem::size_of::<PoolFreed>(), DUMMY_BLOCK_SIZE).unwrap();
    assert_eq!(p.element_size, mem::size_of::<PoolFreed>());
    pool_free_pool(&mut p);

    // block_size == 0
    pool_initialize(&mut p, 8, 0).unwrap();
    assert_eq!(p.block_size, 0);
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_free_all_resets_fields() {
    let mut p = Pool::default();
    pool_initialize(&mut p, 8, DUMMY_BLOCK_SIZE).unwrap();
    p.used = 123;
    p.block = 5;
    unsafe {
        p.freed = alloc_pool_freed();
    }
    pool_free_all(&mut p);
    assert_eq!(p.used, p.block_size as isize - 1);
    assert_eq!(p.block, -1);
    assert!(p.freed.is_null());
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_malloc_alloc_and_expand() {
    let mut p = Pool::default();
    pool_initialize(&mut p, 8, 2).unwrap();

    // Fill up first block to force expansion
    let mut ptrs: [*mut u8; 5] = [ptr::null_mut(); 5];
    for i in 0..5 {
        ptrs[i] = pool_malloc(&mut p);
        assert!(!ptrs[i].is_null());
    }

    // Free a few and make sure pool_free adds to free list
    pool_free(&mut p, ptrs[2]);
    pool_free(&mut p, ptrs[3]);

    // Reuse freed pointers
    let a = pool_malloc(&mut p);
    assert_eq!(a, ptrs[3]); // LIFO free list
    let b = pool_malloc(&mut p);
    assert_eq!(b, ptrs[2]);
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_free_pool_handles_null_blocks() {
    let mut p = Pool::default();
    p.blocks_used = 3;
    p.blocks = vec![std::ptr::null_mut(); p.blocks_used];
    unsafe {
        let layout = std::alloc::Layout::from_size_align(16, 8).unwrap();
        p.blocks[0] = std::alloc::alloc(layout);
    }
    p.blocks[1] = ptr::null_mut();
    // pool_free_pool should not panic
    pool_free_pool(&mut p);
}

#[test]
fn test_realloc_blocks() {
    let mut p = Pool::default();
    pool_initialize(&mut p, 8, 1).unwrap();
    for _ in 0..6 {
        let x = pool_malloc(&mut p);
        assert!(!x.is_null());
    }
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_free_double_free() {
    let mut p = Pool::default();
    pool_initialize(&mut p, 8, 2).unwrap();
    let ptr = pool_malloc(&mut p);
    pool_free(&mut p, ptr);
    // Free the same pointer again -- should add to freelist or be no-op
    pool_free(&mut p, ptr);
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_malloc_without_blocks() {
    let mut p = Pool {
        element_size: 8,
        block_size: 1,
        blocks_used: 1,
        blocks: vec![ptr::null_mut()],
        block: -1,
        used: 0,
        freed: ptr::null_mut(),
        ..Default::default()
    };
    // Simulate calling poolMalloc when block needs to be incremented
    let ptr = pool_malloc(&mut p);
    assert!(!ptr.is_null());
    pool_free_pool(&mut p);
}

#[test]
fn test_pool_free_pool_no_blocks() {
    let mut p = Pool::default();
    // pool.blocks is empty, blocks_used is 0
    // pool_free_pool should not panic
    pool_free_pool(&mut p);
}