use rvrsh3ll_bof_collection::port_is_open_public;

#[test]
fn public_portscan_test_case1() {
    assert_eq!(port_is_open_public("8.8.8.8", 443), 1);
    assert_eq!(port_is_open_public("8.8.8.8", 22), 0);
    println!("public_portscan_test_case1 passed");
}

#[test]
fn public_portscan_test_case2() {
    assert_eq!(port_is_open_public("1.1.1.1", 80), 0);
    assert_eq!(port_is_open_public("1.1.1.1", 853), 1);
    println!("public_portscan_test_case2 passed");
}

#[test]
fn public_portscan_test_case3() {
    assert_eq!(port_is_open_public("127.0.0.1", 65535), 0);
    println!("public_portscan_test_case3 (edge case) passed");
}