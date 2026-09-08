use gc_demo::common::node::Node;
use gc_demo::gc::allocate::allocate;
use gc_demo::refcount::refcount::{refcount_inc, refcount_dec};

#[test]
fn test_refcount_create_and_dec() {
    let n = allocate();
    
    // Test basic ref inc/dec logic
    refcount_inc(&n);
    refcount_dec(&n); // should not free
    refcount_dec(&n); // may free
}

#[test]
fn test_refcount_cycle() {
    let mut n1 = allocate();
    let mut n2 = allocate();
    
    n1.left = Some(n2.clone());
    n2.right = Some(n1.clone());
    
    // Test circular references
    refcount_inc(&n1);
    refcount_inc(&n2);
    refcount_dec(&n1);
    refcount_dec(&n2);
    refcount_dec(&n1);
    refcount_dec(&n2);
    
    println!("refcount/test_refcount: PASS");
}