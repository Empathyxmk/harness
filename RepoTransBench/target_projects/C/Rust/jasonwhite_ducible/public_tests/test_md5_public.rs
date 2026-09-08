use md5::{Md5, Digest};

fn md5_to_hex(digest: &[u8]) -> String {
    digest.iter().map(|b| format!("{:02x}", b)).collect()
}

macro_rules! test_cond {
    ($cond:expr, $name:expr, $fails:ident) => {
        if !$cond {
            println!("{} failed!", $name);
            $fails += 1;
        }
    };
}

#[test]
fn public_md5_tests() {
    let mut fails = 0;

    // Test 1: Different short string
    let str1 = b"Goodbye, world!";
    let digest1 = Md5::digest(str1);
    let hex1 = md5_to_hex(&digest1);
    let expected1 = "f2e0b5c675a1962fa2a343b3bf3f1e49";
    test_cond!(hex1 == expected1, "MD5(\"Goodbye, world!\")", fails);

    // Test 2: Chunked update, different chunked string
    let chunk2a = b"chunk";
    let chunk2b = b"wise";
    let chunk2c = b"Md5";
    let mut ctx2 = Md5::new();
    ctx2.update(chunk2a);
    ctx2.update(chunk2b);
    ctx2.update(chunk2c);
    let digest2 = ctx2.finalize();
    let hex2 = md5_to_hex(&digest2);
    let expected2 = "437dfce14c812c3f05d10d5cbf95c3a7";
    test_cond!(hex2 == expected2, "MD5(chunked \"chunkwiseMd5\")", fails);

    // Test 3: Long string with different character and repeating pattern
    let mut long_str3 = vec![0u8; 1000];
    for i in 0..1000 {
        long_str3[i] = if i % 2 == 0 { b'B' } else { b'a' };
    }
    let digest3 = Md5::digest(&long_str3);
    let hex3 = md5_to_hex(&digest3);
    let expected3 = "74348040e6abdbbfab7d1cf8b7009629";
    test_cond!(hex3 == expected3, "MD5(long public string)", fails);

    // Test 4: Uppercase multi-char string, not in prior test
    let str4 = b"PUBLICMD5TEST";
    let digest4 = Md5::digest(str4);
    let hex4 = md5_to_hex(&digest4);
    let expected4 = "fa9dfb5da104b2d8503d2259ba997244";
    test_cond!(hex4 == expected4, "MD5(\"PUBLICMD5TEST\")", fails);

    if fails == 0 {
        println!("All MD5 public tests passed!");
    } else {
        panic!("{} MD5 public tests failed!", fails);
    }
}