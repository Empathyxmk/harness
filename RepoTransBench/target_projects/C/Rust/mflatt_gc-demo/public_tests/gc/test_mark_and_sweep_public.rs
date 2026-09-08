use gc_demo::common::node::Node;
use gc_demo::gc::allocate::allocate;
use gc_demo::gc::mark_and_sweep::{mark_and_sweep_from_roots, NUM_ROOTS, ROOT_ADDRS};

#[test]
fn test_mark_and_sweep_no_roots_public() {
    unsafe {
        NUM_ROOTS = 0;
        mark_and_sweep_from_roots();
    }
}

#[test]
fn test_mark_and_sweep_one_root_public() {
    unsafe {
        NUM_ROOTS = 1;
        let mut n = allocate();
        let left_node = allocate();
        n.left = Some(left_node);
        n.left.as_mut().unwrap().right = Some(n.clone());
        
        let mut n_ref = Some(n);
        ROOT_ADDRS[0] = &mut n_ref as *mut Option<Box<Node>>;
        
        mark_and_sweep_from_roots();
        
        // Clean up
        ROOT_ADDRS[0] = std::ptr::null_mut();
    }
}

#[test]
fn test_mark_and_sweep_multiple_null_roots_public() {
    unsafe {
        NUM_ROOTS = 3;
        let mut n1: Option<Box<Node>> = None;
        let mut n2: Option<Box<Node>> = None;
        let mut n3: Option<Box<Node>> = None;
        
        ROOT_ADDRS[0] = &mut n1 as *mut Option<Box<Node>>;
        ROOT_ADDRS[1] = &mut n2 as *mut Option<Box<Node>>;
        ROOT_ADDRS[2] = &mut n3 as *mut Option<Box<Node>>;
        
        mark_and_sweep_from_roots();
        
        // Clean up
        ROOT_ADDRS[0] = std::ptr::null_mut();
        ROOT_ADDRS[1] = std::ptr::null_mut();
        ROOT_ADDRS[2] = std::ptr::null_mut();
    }
    
    println!("gc/test_mark_and_sweep_public: PASS");
}