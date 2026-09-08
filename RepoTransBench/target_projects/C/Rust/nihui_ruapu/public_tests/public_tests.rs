use nihui_ruapu::{init, supports, rua};

#[test]
fn test_supports_known_public() {
    init();
    // Use different ISAs than in test_ruapu.c
    let _ = supports("sse2");
    let _ = supports("avx512f");
    let _ = supports("sha1");
    let _ = supports("sm4");
}

#[test]
fn test_supports_unknown_public() {
    init();
    let notfound = supports("foobar_unknown_isa");
    assert!(!notfound); // Unknown ISA should not be supported
}

#[test]
fn test_rua_public() {
    init();
    let arr = rua();
    assert!(!arr.is_empty());
    
    // In Rust we have a proper Vec
    assert!(arr.len() < 1024); // Defensive, different from main test
}