// Rust translation of kernel/lib/skb_array_test01.c
// This is a logical, API/unit-level translation.

#[derive(Debug)]
struct SkbArray<T> {
    ring: Vec<Option<T>>,
    size: usize,
    head: usize,
    tail: usize,
    count: usize,
}

// Simulates only main behaviors from C with Option for emptiness
impl<T> SkbArray<T> {
    fn new(size: usize) -> Self {
        Self {
            ring: vec![None; size],
            size,
            head: 0,
            tail: 0,
            count: 0,
        }
    }

    fn init(&mut self, size: usize) -> Result<(), ()> {
        self.ring = vec![None; size];
        self.size = size;
        self.head = 0;
        self.tail = 0;
        self.count = 0;
        Ok(())
    }

    fn cleanup(&mut self) {
        self.ring = vec![];
        self.count = 0;
    }

    fn produce(&mut self, val: T) -> Result<(), ()> {
        if self.count >= self.size {
            return Err(());
        }
        self.ring[self.tail] = Some(val);
        self.tail = (self.tail + 1) % self.size;
        self.count += 1;
        Ok(())
    }

    fn consume(&mut self) -> Option<T> {
        if self.count == 0 {
            return None;
        }
        let v = self.ring[self.head].take();
        self.head = (self.head + 1) % self.size;
        self.count -= 1;
        v
    }

    fn resize(&mut self, new_size: usize) -> Result<(), ()> {
        // Shrink only for our test; drop excess tail elements
        if new_size < self.count {
            // Remove oldest (head) until only new_size remain
            let remove_ct = self.count - new_size;
            for _ in 0..remove_ct {
                self.consume();
            }
        }
        self.ring.resize(new_size, None);
        self.size = new_size;
        if self.count > new_size {
            self.count = new_size;
        }
        Ok(())
    }
}

// Test: basic init and cleanup
#[test]
fn test_basic_init_and_cleanup() {
    let mut queue = SkbArray::<i32>::new(42);
    assert_eq!(queue.size, 42);
    // MST argued size should not be rounded up
    assert_eq!(queue.ring.len(), 42);
    queue.cleanup();
    assert_eq!(queue.ring.len(), 0);
}

// Test: add and remove object
#[test]
fn test_basic_add_and_remove_object() {
    let mut queue = SkbArray::<i32>::new(123);
    let skb = 42i32;
    queue.produce(skb).expect("produce failed");
    let nskb = queue.consume();
    assert_eq!(nskb, Some(skb));
    queue.cleanup();
}

// Test: queue full condition
#[test]
fn test_queue_full_condition() {
    const Q_SIZE: usize = 33;
    let mut queue = SkbArray::<i32>::new(Q_SIZE);
    let mut i = 0;
    // Try to enqueue more than queue size; should get Err after full
    for idx in 0..(Q_SIZE * 2) {
        let res = queue.produce(100 + idx as i32);
        if res.is_err() {
            break;
        }
        i += 1;
    }
    assert_eq!(i, Q_SIZE);
    queue.cleanup();
}

// Test: queue empty condition and over-dequeue
#[test]
fn test_queue_empty_condition() {
    const Q_SIZE: usize = 4;
    let mut queue = SkbArray::<i32>::new(Q_SIZE);
    // Try to consume from empty queue (should be None)
    let nskb = queue.consume();
    assert!(nskb.is_none());
    // Enqueue 1, dequeue 2
    queue.produce(42).expect("enqueue failed");
    let _nskb2 = queue.consume();
    let nskb3 = queue.consume();
    assert!(nskb3.is_none());
    queue.cleanup();
}

// Test: queue resize/shrink removes excess and works
#[test]
fn test_queue_resize() {
    const Q_SIZE: usize = 34;
    let mut queue = SkbArray::<i32>::new(Q_SIZE);
    // Fill up
    for _ in 0..Q_SIZE {
        queue.produce(100).expect("produce failed");
    }
    // Shrink
    queue.resize(Q_SIZE / 2).expect("resize failed");
    assert_eq!(queue.size, Q_SIZE / 2);
    queue.cleanup();
}