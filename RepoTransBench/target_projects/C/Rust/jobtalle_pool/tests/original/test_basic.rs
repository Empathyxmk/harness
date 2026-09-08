//! Basic pool tests (translated from test.c)

use jobtalle_pool::*;

const SUCCESS: i32 = 0;
const FAILURE: i32 = -1;

fn test_pool(element_size: usize, block_size: usize) -> i32 {
    let mut pool_ptr = Pool::default();
    let test_ptr1 = pool_malloc_checked(&mut pool_ptr, element_size, block_size);
    let test_ptr2 = pool_malloc(&mut pool_ptr);
    // test allocated memory validity
    if test_ptr1.is_null() || test_ptr2.is_null() {
        println!("memory allocation failure");
        return FAILURE;
    }
    pool_free(&mut pool_ptr, test_ptr1);
    pool_free_pool(&mut pool_ptr);
    SUCCESS
}

/// Helper to combine init+alloc as in original C
fn pool_malloc_checked(pool: &mut Pool, element_size: usize, block_size: usize) -> *mut u8 {
    pool_initialize(pool, element_size, block_size).unwrap();
    pool_malloc(pool)
}

#[test]
fn test_pool_4_8() {
    assert_eq!(test_pool(4, 8), SUCCESS);
}
#[test]
fn test_pool_8_8() {
    assert_eq!(test_pool(8, 8), SUCCESS);
}
#[test]
fn test_pool_16_8() {
    assert_eq!(test_pool(16, 8), SUCCESS);
}
#[test]
fn test_pool_32_8() {
    assert_eq!(test_pool(32, 8), SUCCESS);
}