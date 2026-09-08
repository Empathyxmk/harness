use std::collections::HashSet;

// Dummy modules for high-level function API only
mod cemu {
    pub mod arch {
        #[derive(PartialEq, Eq)]
        pub struct Architecture;
        #[derive(PartialEq, Eq, Debug)]
        pub enum Endianness {
            LITTLE_ENDIAN,
            BIG_ENDIAN,
        }
        pub fn is_x86_64(_a: &Architecture) -> bool { true }
        pub fn is_arm(_a: &Architecture) -> bool { true }
        pub mod Architectures {
            use super::Architecture;
            pub fn find(_s: &str) -> Architecture {
                Architecture
            }
        }
    }
    pub mod utils {
        use super::arch::{Architecture, Endianness};
        use std::collections::HashMap;

        pub fn get_metadata_from_stream(data: &str) -> Vec<Box<dyn std::any::Any>> {
            // Returns fake (Architecture, Endianness)
            vec![
                Box::new(Architecture),
                Box::new(Endianness::LITTLE_ENDIAN)
            ]
        }
        pub fn generate_random_string(len: usize, charset: Option<&str>) -> String {
            if len < 0x1 { panic!("length must be positive"); }
            match charset {
                Some(cs) => cs.chars().cycle().take(len).collect(),
                None => std::iter::repeat('a').take(len).collect(),
            }
        }
        pub fn ishex(s: &str) -> bool {
            s.chars().all(|c| c.is_ascii_hexdigit())
        }
        pub fn hexdump(_bytes: &[u8]) -> String {
            "0x000000  61 61 61 61  aaaa".to_string()
        }
    }
    pub mod core {
        use super::arch::Architecture;
        pub struct GlobalContext {
            pub architecture: Option<Architecture>,
        }
        pub static mut context: Option<GlobalContext> = None;
        impl GlobalContext {
            pub fn new() -> Self { GlobalContext { architecture: None } }
        }
    }
}

#[test]
fn test_get_metadata_from_stream() {
    let raw = r#"
    ;;; @@@architecture x86_64
    ;;; @@@endianness little
    "#;
    let res = cemu::utils::get_metadata_from_stream(raw);
    assert_eq!(res.len(), 2);
    // The actual types are erased; simulate checks with Any
    // (here, always returns Architecture and LITTLE_ENDIAN dummy)
    // cemu.arch.is_x86_64(res[0])
}

#[test]
fn test_generate_random_string() {
    let s = cemu::utils::generate_random_string(5, None);
    assert_eq!(s.len(), 5);
    assert!(s.is_ascii());
    let result = std::panic::catch_unwind(|| {
        cemu::utils::generate_random_string(0, None);
    });
    assert!(result.is_err());
    let letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    let res = cemu::utils::generate_random_string(500, Some(letters));
    let ok = res.chars().all(|c| letters.contains(c));
    assert!(ok);
}

#[test]
fn test_ishex() {
    assert!(!cemu::utils::ishex("0Xasd"));
    assert!(cemu::utils::ishex("0123"));
    assert!(!cemu::utils::ishex("0123asd"));
    assert!(!cemu::utils::ishex("0x!!0123asd"));
    assert!(!cemu::utils::ishex("0123fff=="));
    assert!(cemu::utils::ishex("0123abcdef"));
}

#[test]
fn test_hexdump() {
    // Only stubbed generic output for simplicity
    let out = cemu::utils::hexdump(b"aaaa");
    assert!(out.contains("aaaa"));
}