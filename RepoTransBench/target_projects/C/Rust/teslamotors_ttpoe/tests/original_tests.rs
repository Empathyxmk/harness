use ttpoe::{KernelParam, ttp_param_dummy_set, ttp_tag_index_hash_get, 
           ttp_tag_index_vci_get, ttp_tag_index_gwf_get};
use std::fmt::Write;

#[test]
fn test_param_set() {
    let k1 = KernelParam { name: "foo".to_string() };
    let r = ttp_param_dummy_set("bar", Some(&k1));
    assert_eq!(r, -2);

    // Test error on null pointer
    assert_eq!(ttp_param_dummy_set("bar", None), -1);
    
    println!("Param edge/error logic OK.");
}

#[test]
fn test_hash_vci_gwf() {
    let vals = [
        0u64, 
        1u64, 
        0xFFFFFFFFFFFFFFFFu64, 
        1234567890123456789u64, 
        0x8000000000000000u64
    ];
    
    for kid in vals {
        let hval = ttp_tag_index_hash_get(kid);
        let vval = ttp_tag_index_vci_get(kid);
        let gval = ttp_tag_index_gwf_get(kid);
        
        // Just test that functions are deterministic and cover value ranges
        assert_eq!(hval, ttp_tag_index_hash_get(kid));
        assert_eq!(vval, (kid & 0xF) as u8);
        assert_eq!(gval, ((kid >> 4) & 0xF) as u8);
        
        // Print for branch coverage (varied paths)
        println!("KID: {:016x} => hash:{} vci:{} gwf:{}", 
                 kid, hval, vval, gval);
    }
    
    println!("All tag hash/index tests passed.");
}

#[test]
fn test_snprintf_overflow() {
    let mut buf = [0u8; 32];
    let bs = buf.len();
    let mut sc = 0;

    // Similar to the C snprintf - writing formatted string to buffer
    let nn = format!("Hello {}", 7).as_bytes()
        .iter()
        .take(bs - sc)
        .enumerate()
        .map(|(i, &b)| {
            buf[sc + i] = b;
            1
        })
        .sum::<usize>();
    
    if nn <= 0 || nn >= (bs - sc) {
        assert!(false, "Should not overflow");
    }
    sc += nn;

    let nn = " End".as_bytes()
        .iter()
        .take(bs - sc)
        .enumerate()
        .map(|(i, &b)| {
            buf[sc + i] = b;
            1
        })
        .sum::<usize>();
    
    if nn <= 0 || nn >= (bs - sc) {
        assert!(false, "Should not overflow");
    }
    sc += nn;
    
    // This should not overflow
    assert_eq!(&buf[0..sc], "Hello 7 End".as_bytes());

    // Now force an overflow
    sc = 28; // near buffer end
    let nn = "toolongforbuffer".as_bytes()
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
    
    println!("TTP_SNPRINTF logic edge cases passed");
}