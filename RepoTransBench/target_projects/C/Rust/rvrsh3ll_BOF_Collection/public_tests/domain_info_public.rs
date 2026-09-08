use rvrsh3ll_bof_collection::get_domain_info_public;

#[test]
fn public_test_case1() {
    let mut sid = [0u8; 64];
    let ret = get_domain_info_public("public.domain.com", &mut sid, sid.len());
    assert_eq!(ret, 0);
    
    let sid_str = std::str::from_utf8(&sid[..sid.iter().position(|&c| c == 0).unwrap_or(sid.len())])
        .unwrap_or("invalid utf8");
    assert_eq!(sid_str, "S-1-5-21-public");
    
    println!("public_test_case1 passed");
}

#[test]
fn public_test_case2() {
    let mut sid = [0u8; 64];
    let ret = get_domain_info_public("example.com", &mut sid, sid.len());
    assert_eq!(ret, 0);
    
    let sid_str = std::str::from_utf8(&sid[..sid.iter().position(|&c| c == 0).unwrap_or(sid.len())])
        .unwrap_or("invalid utf8");
    assert_eq!(sid_str, "S-1-5-21-example");
    
    println!("public_test_case2 passed");
}

#[test]
fn public_test_case3() {
    let mut sid = [0u8; 64];
    let ret = get_domain_info_public("doesnotexist.local", &mut sid, sid.len());
    assert_ne!(ret, 0);
    
    println!("public_test_case3 (failure scenario) passed");
}