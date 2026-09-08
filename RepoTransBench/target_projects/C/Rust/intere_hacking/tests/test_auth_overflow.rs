use intere_hacking::check_authentication;

#[test]
fn test_valid_brillig() {
    let result = check_authentication("brillig");
    assert_eq!(result, true, "FAIL: brillig should authenticate");
    println!("PASS: brillig");
}

#[test]
fn test_valid_outgrabe() {
    let result = check_authentication("outgrabe");
    assert_eq!(result, true, "FAIL: outgrabe should authenticate");
    println!("PASS: outgrabe");
}

#[test]
fn test_invalid_pass() {
    let result = check_authentication("xyz");
    assert_eq!(result, false, "FAIL: xyz should not authenticate");
    println!("PASS: xyz");
}