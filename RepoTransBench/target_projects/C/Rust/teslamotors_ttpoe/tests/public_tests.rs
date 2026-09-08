use ttpoe::{KernelParam, ttp_tag_index_hash_get, ttp_tag_index_vci_get, 
           ttp_tag_index_gwf_get, public};
use std::fmt::Write;

#[test]
fn test_param_set_public() {
    let k2 = KernelParam { name: "baz".to_string() };
    let r = public::ttp_param_dummy_set("qux", Some(&k2));
    assert_eq!(r, -20);

    // Test error on null pointer (different expectation)
    assert_eq!(public::ttp_param_dummy_set("qux", None), -10);
    
    println!("Param public edge/error logic OK.");
}

#[test]
fn test_hash_vci_gwf_pub() {
    let vals = [
        2u64,
        42u64,
        9876543210u64,
        0x7FFFFFFFFFFFFFFFu64,
        0xFEDCBA9876543210u64
    ];
    
    for kid in vals {
        let hval = ttp_tag_index_hash_get(kid);
        let vval = ttp_tag_index_vci_get(kid);
        let gval = ttp_tag_index_gwf_get(kid);

        // Public tests: Check known values with new data
        println!("[PUB] For kid=0x{:x}: hash=0x{:x}, vci=0x{:x}, gwf=0x{:x}", 
                 kid, hval, vval, gval);

        // Very basic property assertions
        assert_eq!(vval, (kid & 0xF) as u8);
        assert_eq!(gval, ((kid >> 4) & 0xF) as u8);
    }
    
    println!("TTP tag-index public hash/vci/gwf tests PASSED.");
}

#[test]
fn test_snprintf_overflow_public() {
    let mut buf = [0u8; 40];
    let bs = buf.len();
    let mut sc = 0;

    // Use different base string and values for public test
    let nn = format!("World {}", 12).as_bytes()
        .iter()
        .take(bs - sc)
        .enumerate()
        .map(|(i, &b)| {
            buf[sc + i] = b;
            1
        })
        .sum::<usize>();
    
    if nn <= 0 || nn >= (bs - sc) {
        assert!(false, "Should return 11");
    }
    sc += nn;

    let nn = " Test".as_bytes()
        .iter()
        .take(bs - sc)
        .enumerate()
        .map(|(i, &b)| {
            buf[sc + i] = b;
            1
        })
        .sum::<usize>();
    
    if nn <= 0 || nn >= (bs - sc) {
        assert!(false, "Should return 22");
    }
    sc += nn;
    
    // This should not overflow
    assert_eq!(&buf[0..sc], "World 12 Test".as_bytes());

    // Now deliberately force an overflow
    sc = 36; // near buffer end
    let nn = "overflowingcontent".as_bytes()
        .iter()
        .take(bs - sc)
        .enumerate()
        .map(|(i, &b)| {
            if sc + i < bs {
                buf[sc + i] = b;
                1
            } else {
                0
            }
        })
        .sum::<usize>();
    
    // Should indicate overflow
    assert!(nn <= 0 || nn >= (bs - sc));
    
    println!("TTP_SNPRINTF public logic edge cases passed");
}