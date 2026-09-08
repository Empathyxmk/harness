// Translated from buddy2_test.c
use wuwenbin_buddy2::Buddy2;

fn assert_eq_report<T: std::fmt::Debug + PartialEq>(actual: T, expected: T) {
    assert_eq!(actual, expected, "ASSERT FAILED: {} != {}", format!("{:?}", actual), format!("{:?}", expected));
}

fn assert_true_report<T: std::fmt::Debug + PartialEq + std::ops::Not<Output=bool>>(actual: T) where bool: From<T> {
    assert!(bool::from(actual), "ASSERT FAILED (expected true): {:?}", actual);
}

#[test]
fn test_buddy2_new_destroy() {
    // Test invalid size (<1)
    let b = Buddy2::new(0);
    assert_eq_report(b.is_none(), true);

    // Test invalid size (not power of 2)
    let b = Buddy2::new(30);
    assert_eq_report(b.is_none(), true);

    // Correct size
    let b = Buddy2::new(16);
    assert_eq_report(b.is_some(), true);
    if let Some(b) = b {
        b.destroy();
    }
}

#[test]
fn test_buddy2_alloc_basic() {
    let mut b = Buddy2::new(8).expect("buddy2_new(8) should succeed");

    // Should fully allocate
    let o1 = b.alloc(1);
    assert!(o1 >= 0, "Expected o1 >= 0, got {}", o1);
    let o2 = b.alloc(2);
    assert!(o2 >= 0, "Expected o2 >= 0, got {}", o2);
    let o3 = b.alloc(3); // Not power of 2, should round to 4
    assert!(o3 >= 0, "Expected o3 >= 0, got {}", o3);
    let o4 = b.alloc(2);
    // Only 1 block left, 2 is too big, should fail
    assert_eq!(o4, -1);

    b.destroy();
}

#[test]
fn test_buddy2_alloc_edge_cases() {
    let mut b = Buddy2::new(4).expect("buddy2_new(4) should succeed");

    // Allocate with size 0 (should become 1)
    let o = b.alloc(0);
    assert!(o >= 0, "Expected o >= 0, got {}", o);

    // Try to allocate more than available
    let o2 = b.alloc(8);
    assert_eq!(o2, -1);

    // Try NULL pointer
    // Equivalent: Call alloc on None (simulate)
    let none_b: Option<&mut Buddy2> = None;
    let o3 = match none_b {
        Some(ref mut buddy) => buddy.alloc(2),
        None => -1,
    };
    assert_eq!(o3, -1);

    b.destroy();
}

#[test]
fn test_buddy2_free_and_size() {
    let mut b = Buddy2::new(8).expect("buddy2_new(8) should succeed");

    let o1 = b.alloc(4);
    let o2 = b.alloc(2);
    let o3 = b.alloc(1);

    // Free second alloc and check re-allocation
    b.free(o2);

    let o4 = b.alloc(2);
    assert_eq!(o4, o2); // Should get the same spot

    // Buddy2_size for allocated block
    let sz = b.size(o1);
    assert_eq!(sz, 4);

    // Buddy2_size for smallest block
    let sz = b.size(o3);
    assert_eq!(sz, 1);

    b.destroy();
}

#[test]
fn test_buddy2_alloc_free_full_cycle() {
    let mut b = Buddy2::new(4).expect("buddy2_new(4) should succeed");

    // Fully allocate and free all, check all state resets
    let o1 = b.alloc(2);
    let o2 = b.alloc(2);

    // All memory should be used up
    let failed_alloc = b.alloc(1);
    assert_eq!(failed_alloc, -1);

    // Free both, try again
    b.free(o1);
    b.free(o2);

    let o3 = b.alloc(4); // Should get entire block
    assert!(o3 >= 0, "Expected o3 >= 0, got {}", o3);

    b.destroy();
}

#[test]
fn test_buddy2_dump() {
    let b = Buddy2::new(8).expect("buddy2_new(8) should succeed");

    // Simple smoke test (just to touch code, output not validated)
    // buddy2_dump(NULL); // triggers NULL handling (should not panic)
    // In Rust, skip this: passing None does nothing, since method is on instance

    b.dump();

    // Oversize check
    let large = Buddy2::new(128).expect("buddy2_new(128) should succeed");
    large.dump();

    large.destroy();
    b.destroy();
}