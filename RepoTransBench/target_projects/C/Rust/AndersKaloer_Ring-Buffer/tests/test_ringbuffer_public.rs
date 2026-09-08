use ringbuffer::ringbuffer_t;

#[test]
fn test_simple_insertion() {
    let mut buffer = [0u8; 8];
    let mut rb = ringbuffer_t::new(&mut buffer);
    assert_eq!(rb.num_items(), 0);

    // Insert values 10, 20, 30, 40
    assert_eq!(rb.queue(10), true);
    assert_eq!(rb.queue(20), true);
    assert_eq!(rb.queue(30), true);
    assert_eq!(rb.queue(40), true);

    assert_eq!(rb.num_items(), 4);

    // Remove (dequeue) two - should get 10, 20
    let v1 = rb.dequeue().unwrap();
    assert_eq!(v1, 10);
    let v2 = rb.dequeue().unwrap();
    assert_eq!(v2, 20);

    assert_eq!(rb.num_items(), 2);

    // Insert two more values
    assert_eq!(rb.queue(50), true);
    assert_eq!(rb.queue(60), true);
    assert_eq!(rb.num_items(), 4);
}

#[test]
fn test_full_and_empty() {
    let mut buffer = [0u8; 4];
    let mut rb = ringbuffer_t::new(&mut buffer);

    // Fill completely
    assert_eq!(rb.queue(111), true);
    assert_eq!(rb.queue(222), true);
    assert_eq!(rb.queue(88), true);
    assert_eq!(rb.queue(77), false); // Full

    assert_eq!(rb.num_items(), 3);

    // Remove all
    let v1 = rb.dequeue().unwrap();
    assert_eq!(v1, 111);
    let v2 = rb.dequeue().unwrap();
    assert_eq!(v2, 222);
    let v3 = rb.dequeue().unwrap();
    assert_eq!(v3, 88);

    assert_eq!(rb.dequeue(), None);
    assert_eq!(rb.num_items(), 0);
}

#[test]
fn test_wraparound() {
    let mut buffer = [0u8; 3];
    let mut rb = ringbuffer_t::new(&mut buffer);

    // Add and remove to cause wraparound
    assert_eq!(rb.queue(1), true);
    assert_eq!(rb.queue(2), true);
    let v1 = rb.dequeue().unwrap();
    assert_eq!(v1, 1);

    assert_eq!(rb.queue(3), true);
    let v2 = rb.dequeue().unwrap();
    assert_eq!(v2, 2);
    assert_eq!(rb.queue(4), true);

    // Now buffer should hold [3,4]; drain
    let v3 = rb.dequeue().unwrap();
    assert_eq!(v3, 3);
    let v4 = rb.dequeue().unwrap();
    assert_eq!(v4, 4);
    assert_eq!(rb.dequeue(), None); // empty
}

#[test]
fn test_buffer_size_edge() {
    let mut buffer = [0u8; 2];
    let mut rb = ringbuffer_t::new(&mut buffer);

    let data = [42, 17];

    // Only one item of two size can be in buffer
    assert_eq!(rb.queue(data[0]), true);
    assert_eq!(rb.queue(data[1]), false);

    let v1 = rb.dequeue().unwrap();
    assert_eq!(v1, 42);

    assert_eq!(rb.num_items(), 0);
}