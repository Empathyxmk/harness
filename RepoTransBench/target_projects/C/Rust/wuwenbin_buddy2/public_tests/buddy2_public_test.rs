// Translated from buddy2_public_test.c
use wuwenbin_buddy2::Buddy2;

#[test]
fn test_buddy2_new_destroy_public() {
    // Test invalid size (<1)
    let b = Buddy2::new(-5);
    assert_eq!(b.is_none(), true);

    // Test invalid size (not power of 2)
    let b = Buddy2::new(18);
    assert_eq!(b.is_none(), true);

    // Correct size (different from existing test, e.g. 32)
    let b = Buddy2::new(32);
    assert_eq!(b.is_some(), true);
    if let Some(b) = b {
        b.destroy();
    }
}

#[test]
fn test_buddy2_alloc_basic_public() {
    let mut b = Buddy2::new(16).expect("buddy2_new(16) should succeed");

    // Should fully allocate
    let o1 = b.alloc(2);
    assert!(o1 >= 0, "Expected o1 >= 0, got {}", o1);
    let o2 = b.alloc(4);
    assert!(o2 >= 0, "Expected o2 >= 0, got {}", o2);
    let o3 = b.alloc(5); // Not power of 2, should round to 8
    assert!(o3 >= 0, "Expected o3 >= 0, got {}", o3);
    let o4 = b.alloc(4);
    // Not enough space left for another 4, should fail
    assert_eq!(o4, -1);

    b.destroy();
}

#[test]
fn test_buddy2_alloc_edge_cases_public() {
    let mut b = Buddy2::new(2).expect("buddy2_new(2) should succeed");

    // Allocate with size 0 (should become 1)
    let o = b.alloc(0);
    assert!(o >= 0, "Expected o >= 0, got {}", o);

    // Try to allocate more than available
    let o2 = b.alloc(16);
    assert_eq!(o2, -1);

    // Try NULL pointer (simulate by not calling on Option)
    let none_b: Option<&mut Buddy2> = None;
    let o3 = match none_b {
        Some(ref mut buddy) => buddy.alloc(1),
        None => -1,
    };
    assert_eq!(o3, -1);

    b.destroy();
}

#[test]
fn test_buddy2_free_and_size_public() {
    let mut b = Buddy2::new(16).expect("buddy2_new(16) should succeed");

    let o1 = b.alloc(8);
    let o2 = b.alloc(4);
    let o3 = b.alloc(2);

    // Free second alloc and check re-allocation
    b.free(o2);

    let o4 = b.alloc(4);
    assert_eq!(o4, o2); // Should get the same spot

    // Buddy2_size for allocated block
    let sz = b.size(o1);
    assert_eq!(sz, 8);

    // Buddy2_size for smallest block
    let sz = b.size(o3);
    assert_eq!(sz, 2);

    b.destroy();
}

#[test]
fn test_buddy2_alloc_free_full_cycle_public() {
    let mut b = Buddy2::new(8).expect("buddy2_new(8) should succeed");

    // Fully allocate and free all, check all state resets
    let o1 = b.alloc(2);
    let o2 = b.alloc(2);
    let o3 = b.alloc(4);

    // All memory should be used up
    let failed_alloc = b.alloc(1);
    assert_eq!(failed_alloc, -1);

    // Free all, try again
    b.free(o1);
    b.free(o2);
    b.free(o3);

    let o4 = b.alloc(8); // Should get entire block
    assert!(o4 >= 0, "Expected o4 >= 0, got {}", o4);

    b.destroy();
}

#[test]
fn test_buddy2_dump_public() {
    let b = Buddy2::new(32).expect("buddy2_new(32) should succeed");

    // Simple smoke test (just to touch code, output not validated)
    b.dump();

    // Oversize check
    let large = Buddy2::new(64).expect("buddy2_new(64) should succeed");
    large.dump();

    large.destroy();
    b.destroy();
}