use nihui_ruapu::{init, supports, rua};

#[test]
fn test_supports_known() {
    init();
    // Try some common ISAs; result is env-dependent, but function path is covered
    let _ = supports("sse");
    let _ = supports("avx2");
    let _ = supports("aes");
}

#[test]
fn test_supports_unknown() {
    init();
    let notfound = supports("not_a_real_isa");
    assert!(!notfound); // Unrecognized should not be supported
}

#[test]
fn test_rua() {
    init();
    let arr = rua();
    assert!(!arr.is_empty());
    
    // At least the output is null-terminated in the C version
    // In Rust we have a proper Vec, so we just check it's not too large
    assert!(arr.len() < 512); // Defensive
}