// Rust translation of kernel/lib/ring_queue_test.c
// This is a logical, API/unit-level translation of the test patterns.

use std::cell::RefCell;
use std::rc::Rc;

// Minimal trait and implementation to simulate a ring queue; actual ring queue logic omitted.
#[derive(Debug)]
struct RingQueue<T> {
    data: Vec<Option<T>>, // Option for empty slots
    capacity: usize,
    head: usize,
    tail: usize,
    count: usize,
}

impl<T> RingQueue<T> {
    fn new(capacity: usize) -> Self {
        assert!(capacity > 0);
        Self {
            data: vec![None; capacity],
            capacity,
            head: 0,
            tail: 0,
            count: 0,
        }
    }

    fn is_power_of_two(x: usize) -> bool {
        x != 0 && (x & (x - 1)) == 0
    }

    fn create(capacity: usize) -> Option<Self> {
        if !Self::is_power_of_two(capacity) {
            None
        } else {
            Some(Self::new(capacity))
        }
    }

    fn enqueue(&mut self, val: T) -> Result<(), ()> {
        if self.count >= self.capacity {
            return Err(());
        }
        self.data[self.tail] = Some(val);
        self.tail = (self.tail + 1) % self.capacity;
        self.count += 1;
        Ok(())
    }

    fn enqueue_bulk(&mut self, vals: &[T]) -> Result<(), ()>
    where
        T: Copy,
    {
        if self.capacity - self.count < vals.len() {
            return Err(());
        }
        for &v in vals {
            self.enqueue(v)?;
        }
        Ok(())
    }

    fn dequeue(&mut self) -> Option<T> {
        if self.count == 0 {
            return None;
        }
        let v = self.data[self.head].take();
        self.head = (self.head + 1) % self.capacity;
        self.count -= 1;
        v
    }

    fn dequeue_bulk(&mut self, out: &mut [Option<T>])
    where
        T: Copy,
    {
        for o in out.iter_mut() {
            *o = self.dequeue();
        }
    }

    fn count(&self) -> usize {
        self.count
    }

    fn empty(&self) -> bool {
        self.count == 0
    }
}

// Test: creation with not-power-of-two should fail
#[test]
fn test_detect_not_power_of_two() {
    assert!(RingQueue::<i32>::create(42).is_none());
    assert!(RingQueue::<i32>::create(32).is_some());
}

// Test: basic alloc and free
#[test]
fn test_alloc_and_free() {
    let queue = RingQueue::<i32>::create(2048);
    assert!(queue.is_some());
}

// Test: enqueue and dequeue single element (SPSC)
#[test]
fn test_spsc_add_and_remove_elem() {
    let mut queue = RingQueue::<i32>::create(128).unwrap();
    let on_stack = 123;
    let obj = on_stack;
    let mut deq_obj: Option<i32>;

    // Enqueue
    queue.enqueue(obj).expect("enqueue failed");
    // Count
    assert_eq!(queue.count(), 1);
    // Dequeue
    deq_obj = queue.dequeue();
    assert!(deq_obj.is_some());
    assert_eq!(deq_obj.unwrap(), obj);
    // Should be empty
    assert!(queue.empty());
}

// Test: enqueue and dequeue bulk
#[test]
fn test_spsc_add_and_remove_elems_bulk() {
    let mut queue = RingQueue::<usize>::create(128).unwrap();
    const BULK: usize = 10;
    let mut objs: [usize; BULK] = [0; BULK];
    for i in 0..BULK {
        objs[i] = i + 20;
    }
    queue.enqueue_bulk(&objs).expect("enqueue_bulk failed");
    assert_eq!(queue.count(), BULK);

    let mut deq_objs: [Option<usize>; BULK] = [None; BULK];
    queue.dequeue_bulk(&mut deq_objs);
    for i in 0..BULK {
        assert_eq!(deq_objs[i], Some(objs[i]));
    }
    assert!(queue.empty());
}

// Test: late void pointer cast simulation with int arrays
#[test]
fn test_late_void_ptr_cast_bulk() {
    let mut queue = RingQueue::<i32>::create(128).unwrap();
    const BULK: usize = 10;
    let objs_data: [i32; BULK] = [21,22,23,24,25,26,27,28,29,30];
    let mut objs: [i32; BULK] = objs_data;
    queue.enqueue_bulk(&objs).expect("enqueue_bulk failed");
    assert_eq!(queue.count(), BULK);
    let mut deq_objs: [Option<i32>; BULK] = [None; BULK];
    queue.dequeue_bulk(&mut deq_objs);
    for i in 0..BULK {
        assert_eq!(deq_objs[i], Some(objs_data[i]));
    }
    assert!(queue.empty());
}