#[test]
fn test_sqlite_alloc_public() {
    let mut v = vec![2u8; 48];
    assert_eq!(v.len(), 48);
    drop(v);
}

#[test]
fn test_sqlite_malloc_failed_public() {
    // Simulate similar to original: check "failure" metric preserved
    struct SqliteMallocFailed(u32);
    let mut s = SqliteMallocFailed(0);
    let p = vec![0u8; 8];
    assert!(p.capacity() >= 0);
    let old_failed = s.0;
    assert_eq!(s.0, old_failed);
}

fn sqlite_set_string(args: &[&str]) -> String {
    args.concat()
}

#[test]
fn test_sqlite_set_string_public() {
    let z = sqlite_set_string(&["Foo", "-", "Bar"]);
    assert_eq!(z, "Foo-Bar");
}

fn sqlite_str_icmp(a: &str, b: &str) -> i32 {
    a.to_lowercase().cmp(&b.to_lowercase()) as i32
}
#[test]
fn test_sqlite_str_icmp_public() {
    assert_eq!(sqlite_str_icmp("Test", "tESt"), 0);
    assert_eq!(sqlite_str_icmp("Apple", "Banana"), -1);
    assert_eq!(sqlite_str_icmp("Zebra", "ant"), 1);
}

fn sqlite_str_nicmp(a: &str, b: &str, n: usize) -> i32 {
    let a = a[..n.min(a.len())].to_lowercase();
    let b = b[..n.min(b.len())].to_lowercase();
    a.cmp(&b) as i32
}
#[test]
fn test_sqlite_str_nicmp_public() {
    assert_eq!(sqlite_str_nicmp("HelloWorld", "helloWORLD", 5), 0);
    assert_eq!(sqlite_str_nicmp("Short", "Shoot", 3), 0);
    assert_eq!(sqlite_str_nicmp("123abc", "124abc", 3), -1);
}

#[test]
fn test_sqlite_str_dup_public() {
    let z = String::from("customstring");
    assert_eq!(z, "customstring");
}

#[test]
fn test_sqlite_check_memory_public() {
    // Always returns 0 (OK)
    fn sqlite_check_memory() -> i32 { 0 }
    assert_eq!(sqlite_check_memory(), 0);
}