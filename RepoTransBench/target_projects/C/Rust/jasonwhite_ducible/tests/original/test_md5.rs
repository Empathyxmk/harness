use md5::{Md5, Digest};

fn md5_to_hex(digest: &[u8]) -> String {
    digest.iter().map(|b| format!("{:02x}", b)).collect()
}

// Test case: compare MD5 hash output with known values for test vectors.
fn test_md5_vector(msg: &[u8], expected_hex: &str) -> bool {
    let mut hasher = Md5::new();
    hasher.update(msg);
    let result = hasher.finalize();
    let hex = md5_to_hex(&result);
    let ok = hex == expected_hex;
    if !ok {
        println!(
            "MD5({:?}) failed. Got: {}, Expected: {}",
            String::from_utf8_lossy(msg),
            hex,
            expected_hex
        );
    }
    ok
}

#[test]
fn test_md5_empty() {
    assert!(test_md5_vector(b"", "d41d8cd98f00b204e9800998ecf8427e"));
}

#[test]
fn test_md5_a() {
    assert!(test_md5_vector(b"a", "0cc175b9c0f1b6a831c399e269772661"));
}

#[test]
fn test_md5_abc() {
    assert!(test_md5_vector(b"abc", "900150983cd24fb0d6963f7d28e17f72"));
}

#[test]
fn test_md5_64bytes() {
    let msg = vec![b'a'; 64];
    // python: hashlib.md5(b"a"*64).hexdigest() == "014842d480b571495a4a0363793f7367"
    assert!(test_md5_vector(&msg, "014842d480b571495a4a0363793f7367"));
}

#[test]
fn test_md5_chunked() {
    let mut hasher = Md5::new();
    hasher.update(b"abc");
    hasher.update(b"de");
    hasher.update(b"f");
    let result = hasher.finalize();
    let hex = md5_to_hex(&result);
    let expected = "e80b5017098950fc58aad83c8c14978e";
    let ok = hex == expected;
    if !ok {
        println!("MD5(chunked \"abcdef\") failed. Got: {}", hex);
    }
    assert!(ok);
}

#[test]
fn test_md5_restart() {
    // Hasher cannot be restarted in-place, but we can simulate it with new instances.
    // First run: "one"
    let mut hasher = Md5::new();
    hasher.update(b"one");
    let result1 = hasher.finalize_reset();
    let hex1 = md5_to_hex(&result1);

    // Second run: "two"
    hasher.update(b"two");
    let result2 = hasher.finalize();
    let hex2 = md5_to_hex(&result2);

    let ok1 = hex1 == "f97c5d29941bfb1b2fdab0874906ab82";
    let ok2 = hex2 == "b8a9f715dbb64fd5c56e7788e47a9245";
    if !ok1 || !ok2 {
        println!("MD5(restart) failed: {},{}", hex1, hex2);
    }
    assert!(ok1 && ok2);
}

#[test]
fn test_md5_null_update() {
    let mut hasher = Md5::new();
    // Zero-length update
    hasher.update(&[]);
    let result = hasher.finalize();
    let hex = md5_to_hex(&result);
    let expected = "d41d8cd98f00b204e9800998ecf8427e";
    let ok = hex == expected;
    if !ok {
        println!("MD5(NULL,0) failed. Got: {}", hex);
    }
    assert!(ok);
}

#[test]
fn test_md5_partial_block() {
    // 55 bytes (less than 64, so partial block)
    let mut msg = vec![b'X'; 55];
    // no need for trailing null in Rust
    // MD5 of "X"*55: "1ef5c29574d49140e2aef8b5693fd3c1"
    assert!(test_md5_vector(&msg, "1ef5c29574d49140e2aef8b5693fd3c1"));
}

#[test]
fn test_md5_large() {
    // 256 bytes: msg[i] = (i%23 + 41)
    let msg: Vec<u8> = (0..256).map(|i| ((i % 23) + 41) as u8).collect();
    // hashlib.md5(bytes((i%23+41) for i in range(256))).hexdigest(): '7e74c116be21c248b8d5e0d1576e79e0'
    let mut hasher = Md5::new();
    hasher.update(&msg);
    let result = hasher.finalize();
    let hex = md5_to_hex(&result);
    let expected = "7e74c116be21c248b8d5e0d1576e79e0";
    let ok = hex == expected;
    if !ok {
        println!("MD5(large/256) failed. Got: {}", hex);
    }
    assert!(ok);
}