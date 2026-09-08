use rvrsh3ll_bof_collection::go_portscan;

#[test]
fn test_basic_portscan() {
    // Create a buffer with "target\0port" similar to the C test
    let mut buf = Vec::new();
    buf.extend_from_slice(b"target");
    buf.push(0); // Null terminator
    buf.extend_from_slice(b"port");
    
    let result = go_portscan(&buf);
    assert!(result == 0, "Port scan should complete successfully");
}