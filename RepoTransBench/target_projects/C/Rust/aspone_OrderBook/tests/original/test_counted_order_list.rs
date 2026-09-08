// Translated from TestCountedOrderList.h

use std::ptr;

#[derive(Debug)]
struct OrderNode {
    next: *mut OrderNode,
    previous: *mut OrderNode,
    order_qty: u32,
}

impl OrderNode {
    fn new(q: u32) -> Self {
        OrderNode {
            next: ptr::null_mut(),
            previous: ptr::null_mut(),
            order_qty: q,
        }
    }
    fn print_self(&self) {
        eprintln!("{}", self.order_qty);
    }
}

struct CountedOrderList {
    head: *mut OrderNode,
    tail: *mut OrderNode,
    quantity: u32,
}

impl CountedOrderList {
    fn new() -> Self {
        CountedOrderList {
            head: ptr::null_mut(),
            tail: ptr::null_mut(),
            quantity: 0,
        }
    }
    fn add_node(&mut self, node: *mut OrderNode) {
        unsafe {
            (*node).next = self.head;
            (*node).previous = ptr::null_mut();
            if !self.head.is_null() {
                (*self.head).previous = node;
            } else {
                self.tail = node;
            }
            self.head = node;
            self.quantity += (*node).order_qty;
        }
    }

    fn remove_node(&mut self, node: *mut OrderNode) {
        unsafe {
            self.quantity -= (*node).order_qty;
            let next = (*node).next;
            let prev = (*node).previous;
            if !prev.is_null() {
                (*prev).next = next;
            } else {
                self.head = next;
            }
            if !next.is_null() {
                (*next).previous = prev;
            } else {
                self.tail = prev;
            }
            (*node).next = ptr::null_mut();
            (*node).previous = ptr::null_mut();
        }
    }

    fn change_node_quantity(&mut self, node: *mut OrderNode, new_qty: u32) {
        unsafe {
            self.quantity = self.quantity - (*node).order_qty + new_qty;
            (*node).order_qty = new_qty;
        }
    }

    fn get_quantity(&self) -> u32 {
        self.quantity
    }

    fn get_head(&self) -> *mut OrderNode {
        self.head
    }
    fn get_tail(&self) -> *mut OrderNode {
        self.tail
    }

    fn print_level(
        &self,
        _level: char,
        buffer: &mut [u8],
        index: &mut usize,
        _max_buffer: usize,
    ) {
        // For demonstration, just simulate C buffer-write logic
        let mut curr = self.head;
        while !curr.is_null() {
            unsafe {
                let s = format!("{} ", (*curr).order_qty);
                let bytes = s.as_bytes();
                let end = (*index + bytes.len()).min(buffer.len());
                buffer[*index..end].copy_from_slice(&bytes[..end - *index]);
                *index += bytes.len();
                curr = (*curr).next;
            }
        }
    }

    fn clear_level(&mut self) {
        let mut curr = self.head;
        while !curr.is_null() {
            unsafe {
                let next = (*curr).next;
                (*curr).next = ptr::null_mut();
                (*curr).previous = ptr::null_mut();
                curr = next;
            }
        }
        self.head = ptr::null_mut();
        self.tail = ptr::null_mut();
        self.quantity = 0;
    }
}

#[test]
fn test_counted_order_list_basic() {
    let mut list = CountedOrderList::new();
    let mut n1 = Box::new(OrderNode::new(5));
    let mut n2 = Box::new(OrderNode::new(7));

    let n1_ptr = &mut *n1 as *mut OrderNode;
    let n2_ptr = &mut *n2 as *mut OrderNode;

    unsafe {
        list.add_node(n1_ptr);
        assert_eq!(list.get_quantity(), 5);
        list.add_node(n2_ptr);
        assert_eq!(list.get_quantity(), 12);

        list.remove_node(n1_ptr);
        assert_eq!(list.get_quantity(), 7);

        list.change_node_quantity(n2_ptr, 12);
        assert_eq!(list.get_quantity(), 12);

        let mut n3 = Box::new(OrderNode::new(8));
        let n3_ptr = &mut *n3 as *mut OrderNode;
        list.add_node(n3_ptr);

        let bufsize = 100;
        let mut buffer = vec![0u8; bufsize];
        let mut index = 0usize;
        let max_buffer = bufsize;
        list.print_level('a', &mut buffer, &mut index, max_buffer);
        assert!(index > 0);
    }
}

#[test]
fn test_counted_order_list_clear_level() {
    let mut list = CountedOrderList::new();
    let mut n1 = Box::new(OrderNode::new(3));
    let mut n2 = Box::new(OrderNode::new(7));
    let n1_ptr = &mut *n1 as *mut OrderNode;
    let n2_ptr = &mut *n2 as *mut OrderNode;
    unsafe {
        list.add_node(n1_ptr);
        list.add_node(n2_ptr);
        list.clear_level();
        assert_eq!(list.get_quantity(), 0);
        assert!(list.get_head().is_null() && list.get_tail().is_null());
    }
}