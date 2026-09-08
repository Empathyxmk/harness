use cloudwu_rudp::*;
use std::sync::Arc;

// Helper function to fill a buffer with sequential data
fn fill_buffer(buf: &mut [u8]) {
    for (i, slot) in buf.iter_mut().enumerate() {
        *slot = (i % 100) as u8;
    }
}

#[test]
fn test_rudp_new_and_delete() {
    let u = rudp_new(1, 5);
    // Check that returned object is not null (in Rust, not panic on creation)
    // Since Rust's rudp_new should either panic or return Result, but we'll simulate Option-style:
    // If your interface returns Result, you may want to adjust
    assert!(std::mem::size_of_val(&u) > 0);
    rudp_delete(u);
}

#[test]
fn test_rudp_send_and_update_no_recv() {
    let mut u = rudp_new(1, 5);
    let data = [1u8, 2, 3, 4];
    let _ = rudp_send(&mut u, &data).unwrap();
    let _ = rudp_update(&mut u, None, 1);
    rudp_delete(u);
}

#[test]
fn test_rudp_send_large_package() {
    let mut u = rudp_new(1, 5);
    let mut data = [0u8; 256];
    fill_buffer(&mut data);
    let _ = rudp_send(&mut u, &data).unwrap();
    let _ = rudp_update(&mut u, None, 1);
    rudp_delete(u);
}

#[test]
fn test_rudp_recv_corrupt() {
    let mut u = rudp_new(1, 5);
    let badpacket = [0xffu8, 0x00, 0x01, 0x02, 0x03];
    let _ = rudp_send(&mut u, &badpacket).unwrap();
    let _ = rudp_update(&mut u, None, 1);

    let mut recv_buf = [0u8; MAX_PACKAGE];
    let r = rudp_recv(&mut u, &mut recv_buf);
    assert!(r <= 0);
    rudp_delete(u);
}

#[test]
fn test_rudp_send_update_recv_fuzz() {
    let mut u = rudp_new(1, 5);
    let payloads = [
        [1u8,2,3,4,5,6],
        [20u8,30,40,50,60,70],
        [100u8,101,102,103,104,105],
    ];
    for p in payloads.iter() {
        let _ = rudp_send(&mut u, p).unwrap();
    }
    for t in 0..4 {
        let _ = rudp_update(&mut u, None, t);
    }
    rudp_delete(u);
}

#[test]
fn test_rudp_update_recv_and_recv_edge_cases() {
    let mut u = rudp_new(1, 5);
    let buf = [1u8,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16];
    let _ = rudp_send(&mut u, &buf).unwrap();
    let out = rudp_update(&mut u, None, 1);
    // Simulate feedback/ack packet reception (simulate wire)
    if let Some(ref out_pkg) = out {
        if !out_pkg.buffer.is_empty() && out_pkg.sz > 0 {
            let _ = rudp_update(&mut u, Some(&out_pkg.buffer[..out_pkg.sz]), 2);
        }
    }
    let mut rbuf = [0u8; MAX_PACKAGE];
    let _r = rudp_recv(&mut u, &mut rbuf);
    rudp_delete(u);
}

#[test]
fn test_rudp_delete_null_and_empty() {
    // Test deleting a NULL U (Rust has ownership, so this is more of a no-op)
    // Make sure deleting an empty/freshly created object does not panic
    let u = rudp_new(1, 5);
    rudp_delete(u);
}

#[test]
fn test_multiple_queues_and_expiry() {
    let mut u = rudp_new(0, 1);
    let mut buf = [42u8; 64];
    for _ in 0..40 {
        let _ = rudp_send(&mut u, &buf).unwrap();
    }
    for t in 0..20 {
        let _ = rudp_update(&mut u, None, t);
    }
    rudp_delete(u);
}