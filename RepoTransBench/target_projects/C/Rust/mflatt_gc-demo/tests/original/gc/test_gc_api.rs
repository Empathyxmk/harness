use gc_demo::common::mem::mem_init;
use gc_demo::gc::allocate::allocate;
use gc_demo::gc::allocate::collect_garbage;

#[test]
fn test_gc_api_basic() {
    mem_init();
    let _n = allocate();
    collect_garbage();
    
    println!("gc/test_gc_api: PASS");
}