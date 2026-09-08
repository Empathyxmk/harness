// Translation of TestDLList.h to Rust.
// Assumes existence of a DLList implementation for a generic node type.

use std::ptr;

#[derive(Debug)]
struct TestNode {
    next: *mut TestNode,
    previous: *mut TestNode,
    val: i32,
}

impl TestNode {
    fn new(val: i32) -> Self {
        TestNode {
            next: std::ptr::null_mut(),
            previous: std::ptr::null_mut(),
            val,
        }
    }
    fn print_self(&self) {
        eprintln!("{}", self.val);
    }
}

struct DLList<T> {
    head: *mut T,
    tail: *mut T,
}

impl<T> DLList<T> {
    fn new() -> Self {
        DLList {
            head: ptr::null_mut(),
            tail: ptr::null_mut(),
        }
    }
    fn add_node(&mut self, node: *mut T)
    where
        T: NodeLink<T>,
    {
        unsafe {
            (*node).set_next(self.head);
            if !self.head.is_null() {
                (*self.head).set_previous(node);
            }
            (*node).set_previous(ptr::null_mut());
            self.head = node;
            if self.tail.is_null() {
                self.tail = node;
            }
        }
    }

    fn remove_node(&mut self, node: *mut T)
    where
        T: NodeLink<T>,
    {
        unsafe {
            let next = (*node).get_next();
            let prev = (*node).get_previous();

            if !prev.is_null() {
                (*prev).set_next(next);
            } else {
                self.head = next;
            }
            if !next.is_null() {
                (*next).set_previous(prev);
            } else {
                self.tail = prev;
            }
            (*node).set_next(ptr::null_mut());
            (*node).set_previous(ptr::null_mut());
        }
    }

    fn get_head(&self) -> *mut T {
        self.head
    }
    fn get_tail(&self) -> *mut T {
        self.tail
    }
}

// Required to "navigate" next/previous pointers generically
trait NodeLink<T> {
    fn get_next(&self) -> *mut T;
    fn get_previous(&self) -> *mut T;
    fn set_next(&mut self, n: *mut T);
    fn set_previous(&mut self, p: *mut T);
}
impl NodeLink<TestNode> for TestNode {
    fn get_next(&self) -> *mut TestNode {
        self.next
    }
    fn get_previous(&self) -> *mut TestNode {
        self.previous
    }
    fn set_next(&mut self, n: *mut TestNode) {
        self.next = n;
    }
    fn set_previous(&mut self, p: *mut TestNode) {
        self.previous = p;
    }
}

#[test]
fn test_dllist_basic() {
    let mut list = DLList::<TestNode>::new();

    // Note: Use Box to allocate on heap so we can use pointers safely in Rust
    let mut n1 = Box::new(TestNode::new(1));
    let mut n2 = Box::new(TestNode::new(2));
    let mut n3 = Box::new(TestNode::new(3));

    // Get mutable pointers for nodes
    let n1_ptr: *mut TestNode = &mut *n1;
    let n2_ptr: *mut TestNode = &mut *n2;
    let n3_ptr: *mut TestNode = &mut *n3;

    unsafe {
        // Add nodes
        list.add_node(n1_ptr);
        assert_eq!(list.get_head(), n1_ptr);
        assert_eq!(list.get_tail(), n1_ptr);

        list.add_node(n2_ptr);
        assert_eq!(list.get_head(), n2_ptr);
        assert_eq!(list.get_tail(), n1_ptr);

        list.add_node(n3_ptr);
        assert_eq!(list.get_head(), n3_ptr);
        assert_eq!(list.get_tail(), n1_ptr);

        // Remove from middle, head, tail, single
        list.remove_node(n2_ptr); // middle node
        assert_eq!(list.get_head(), n3_ptr);
        assert_eq!(list.get_tail(), n1_ptr);

        list.remove_node(n3_ptr); // head node (with prev!=0)
        assert_eq!(list.get_head(), n1_ptr);
        assert_eq!(list.get_tail(), n1_ptr);

        list.remove_node(n1_ptr); // single-node
        assert!(list.get_head().is_null());
        assert!(list.get_tail().is_null());
    }
}