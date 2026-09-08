//! Public extension test program for memory pool (translated from test_ext_public.c)
use jobtalle_pool::*;
use std::mem;

const SUCCESS: i32 = 0;
const FAILURE: i32 = -1;

#[repr(C)]
struct Point {
    x: i32,
    y: i32,
}

fn fill_point(p: &mut Point, offset: i32) {
    p.x = 1000 + offset;
    p.y = 2000 + offset;
}

#[test]
fn test_ext_public_basic() {
    let mut pool_ptr = Pool::default();

    // Use different element/block sizes than test_ext.c
    let element_size = mem::size_of::<Point>();
    let block_size = 6;

    pool_initialize(&mut pool_ptr, element_size, block_size).unwrap();

    // Allocate several points from the pool
    let p1 = pool_malloc(&mut pool_ptr) as *mut Point;
    let p2 = pool_malloc(&mut pool_ptr) as *mut Point;
    let p3 = pool_malloc(&mut pool_ptr) as *mut Point;

    // Fill data with different patterns
    unsafe {
        fill_point(&mut *p1, 10);
        fill_point(&mut *p2, 20);
        fill_point(&mut *p3, 30);

        assert_eq!((*p1).x, 1010);
        assert_eq!((*p1).y, 2010);
        assert_eq!((*p2).x, 1020);
        assert_eq!((*p2).y, 2020);
        assert_eq!((*p3).x, 1030);
        assert_eq!((*p3).y, 2030);

        // Free one element, allocate again - should recycle slot (address reuse not required)
        pool_free(&mut pool_ptr, p2 as *mut u8);
        let p4 = pool_malloc(&mut pool_ptr) as *mut Point;
        fill_point(&mut *p4, 40);
        assert_eq!((*p4).x, 1040);
        assert_eq!((*p4).y, 2040);
    }

    pool_free_pool(&mut pool_ptr);
}