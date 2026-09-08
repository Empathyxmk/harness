use gc_demo::common::node::Node;
use gc_demo::gc::allocate::allocate;
use gc_demo::gc::mark_and_sweep::{mark_and_sweep_from_roots, NUM_ROOTS, ROOT_ADDRS};

#[test]
fn test_mark_and_sweep_from_roots_handles_no_roots() {
    unsafe {
        NUM_ROOTS = 0;
        mark_and_sweep_from_roots();
    }
}

#[test]
fn test_mark_and_sweep_with_root() {
    unsafe {
        NUM_ROOTS = 1;
        let mut n = allocate();
        ROOT_ADDRS[0] = &mut n as *mut Option<Box<Node>>;
        mark_and_sweep_from_roots();
        // Clean up
        ROOT_ADDRS[0] = std::ptr::null_mut();
    }
}

#[test]
fn test_mark_and_sweep_with_multiple_roots() {
    unsafe {
        NUM_ROOTS = 2;
        let mut n1 = allocate();
        let n2 = allocate();
        n1.right = Some(n2);
        
        let mut n1_ref = Some(n1);
        let mut n2_ref = n1_ref.as_mut().unwrap().right.take();
        
        if let Some(ref mut n2_inner) = n2_ref {
            n2_inner.left = n1_ref.clone();
        }
        
        ROOT_ADDRS[0] = &mut n1_ref as *mut Option<Box<Node>>;
        ROOT_ADDRS[1] = &mut n2_ref as *mut Option<Box<Node>>;
        
        mark_and_sweep_from_roots();
        
        // Clean up
        ROOT_ADDRS[0] = std::ptr::null_mut();
        ROOT_ADDRS[1] = std::ptr::null_mut();
    }
    
    println!("gc/test_mark_and_sweep: PASS");
}