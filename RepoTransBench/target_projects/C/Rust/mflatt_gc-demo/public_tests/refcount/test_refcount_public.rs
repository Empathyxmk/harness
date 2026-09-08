use std::ptr;
use gc_demo::refcount::allocate::allocate;
use gc_demo::refcount::refcount::{rc_init, rc_collect};

#[derive(Debug)]
struct ConsCell {
    value: i32,
    next: *mut ConsCell,
}

fn make_cons(value: i32, next: *mut ConsCell) -> *mut ConsCell {
    let cell: *mut ConsCell = allocate(std::mem::size_of::<ConsCell>());
    unsafe {
        (*cell).value = value;
        (*cell).next = next;
    }
    cell
}

#[test]
fn test_cons_list_3nodes_public() {
    rc_init();
    
    let head = make_cons(200, make_cons(99, make_cons(44, ptr::null_mut())));
    
    unsafe {
        assert!(!head.is_null());
        assert_eq!((*head).value, 200);
        assert!(!(*head).next.is_null());
        assert_eq!((*(*head).next).value, 99);
        assert!(!(*(*head).next).next.is_null());
        assert_eq!((*(*(*head).next).next).value, 44);
        assert!((*(*(*head).next).next).next.is_null());
    }
    
    rc_collect();
    rc_collect(); // extra call, as would GC tests
}

#[test]
fn test_drop_reference_public() {
    rc_init();
    
    let node1 = make_cons(500, ptr::null_mut());
    let node2 = make_cons(700, node1);
    
    // Drop reference to node1 via node2
    unsafe {
        (*node2).next = ptr::null_mut();
    }
    
    rc_collect();
    
    // node2 should still be valid
    unsafe {
        assert_eq!((*node2).value, 700);
    }
}

#[test]
fn test_circular_reference_public() {
    rc_init();
    
    let node_a = make_cons(1024, ptr::null_mut());
    let node_b = make_cons(2048, node_a);
    
    unsafe {
        (*node_a).next = node_b; // cycle: nodeA -> nodeB -> nodeA
    }
    
    // Remove outside references
    let _node_a = ptr::null_mut::<ConsCell>();
    let _node_b = ptr::null_mut::<ConsCell>();
    
    rc_collect();
    
    println!("refcount/test_refcount_public: PASS");
}