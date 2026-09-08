use ringbuffer::RingBuffer;

#[test]
fn test_init_empty() {
    let mut buf = [0u8; 8];
    let rb = RingBuffer::new(&mut buf);
    assert!(rb.is_empty());
}

#[test]
fn test_queue_dequeue_single_char() {
    let mut buf = [0u8; 8];
    let mut rb = RingBuffer::new(&mut buf);
    assert!(rb.queue(b'A'));
    assert!(!rb.is_empty());
    let c = rb.dequeue().unwrap();
    assert_eq!(c, b'A');
    assert!(rb.is_empty());
}

#[test]
fn test_queue_overfill() {
    let mut buf = [0u8; 8];
    let mut rb = RingBuffer::new(&mut buf);
    for i in 0..20 {
        rb.queue(i as u8);
    }
    assert!(rb.is_full() || rb.num_items() == 7);
    let mut count = 0;
    while let Some(_) = rb.dequeue() {
        count += 1;
    }
    assert_eq!(count, 7); // Capacity is 8-1=7
}

#[test]
fn test_queue_arr_and_dequeue_arr() {
    let mut buf = [0u8; 8];
    let src = [1u8, 2, 3, 4, 5];
    let mut out = [0u8; 5];
    let mut rb = RingBuffer::new(&mut buf);
    let queued = rb.queue_arr(&src);
    assert_eq!(queued, 5);
    let n = rb.dequeue_arr(&mut out);
    assert_eq!(n, 5);
    assert_eq!(src, out);
}

#[test]
fn test_peek() {
    let mut buf = [0u8; 8];
    let mut rb = RingBuffer::new(&mut buf);
    for i in 0..4 { rb.queue(b'A' + i as u8); }
    assert_eq!(rb.peek(2), Some(b'C'));
    // Out of range
    assert_eq!(rb.peek(8), None);
}

#[test]
fn test_empty_and_full_conditions() {
    let mut buf = [0u8; 4];
    let mut rb = RingBuffer::new(&mut buf);
    assert!(rb.is_empty());
    rb.queue(1);
    rb.queue(2);
    rb.queue(3); // max 3 for buffer size 4
    assert!(rb.is_full());
    let _ = rb.dequeue();
    assert!(!rb.is_full());
}

#[test]
fn test_dequeue_empty() {
    let mut buf = [0u8; 8];
    let mut rb = RingBuffer::new(&mut buf);
    let mut c = 0x77u8;
    let out = rb.dequeue().unwrap_or(0x77);
    assert_eq!(out, 0x77);
}

#[test]
fn test_dequeue_arr_empty() {
    let mut buf = [0u8; 8];
    let mut out = [0u8; 4];
    let mut rb = RingBuffer::new(&mut buf);
    let ret = rb.dequeue_arr(&mut out);
    assert_eq!(ret, 0);
}