//! Public test: pool with different element/block sizes (translated from test_public.c)
use jobtalle_pool::*;

const SUCCESS: i32 = 0;
const FAILURE: i32 = -1;

fn test_pool(element_size: usize, block_size: usize) -> i32 {
    let mut pool_ptr = Pool::default();
    let test_ptr1 = pool_malloc_checked(&mut pool_ptr, element_size, block_size);
    let test_ptr2 = pool_malloc(&mut pool_ptr);
    // test allocated memory validity
    if test_ptr1.is_null() || test_ptr2.is_null() {
        println!("memory allocation failure (public)");
        return FAILURE;
    }
    pool_free(&mut pool_ptr, test_ptr1);
    pool_free_pool(&mut pool_ptr);
    SUCCESS
}

fn pool_malloc_checked(pool: &mut Pool, element_size: usize, block_size: usize) -> *mut u8 {
    pool_initialize(pool, element_size, block_size).unwrap();
    pool_malloc(pool)
}

#[test]
fn test_public_12_16() {
    assert_eq!(test_pool(12, 16), SUCCESS);
}
#[test]
fn test_public_20_4() {
    assert_eq!(test_pool(20, 4), SUCCESS);
}
#[test]
fn test_public_24_12() {
    assert_eq!(test_pool(24, 12), SUCCESS);
}
#[test]
fn test_public_40_6() {
    assert_eq!(test_pool(40, 6), SUCCESS);
}