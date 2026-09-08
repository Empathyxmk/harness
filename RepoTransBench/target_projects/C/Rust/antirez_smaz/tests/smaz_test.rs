//! Rust port of original smaz_test.c (original test suite)
use smaz::{smaz_compress, smaz_decompress};

use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

#[test]
fn original_smaz_test_suite() {
    let strings = [
        "This is a small string",
        "foobar",
        "the end",
        "not-a-g00d-Exampl333",
        "Smaz is a simple compression library",
        "Nothing is more difficult, and therefore more precious, than to be able to decide",
        "this is an example of what works very well with smaz",
        "1000 numbers 2000 will 10 20 30 compress very little",
        "and now a few italian sentences:",
        "Nel mezzo del cammin di nostra vita, mi ritrovai in una selva oscura",
        "Mi illumino di immenso",
        "L'autore di questa libreria vive in Sicilia",
        "try it against urls",
        "http://google.com",
        "http://programming.reddit.com",
        "http://github.com/antirez/smaz/tree/master",
        "/media/hdb1/music/Alben/The Bla"
    ];
    // Note: NULL terminator not needed in Rust.

    for orig in &strings {
        let input = orig.as_bytes();
        let mut out = [0u8; 4096];
        let mut d = [0u8; 4096];

        let comprlen = smaz_compress(input, &mut out)
            .expect("Compression failed in smaz_test");
        let decomprlen = smaz_decompress(&out[..comprlen], &mut d)
            .expect("Decompression failed in smaz_test");

        assert_eq!(input.len(), decomprlen, "Lengths did not match for '{}'", orig);
        assert_eq!(&input[..], &d[..decomprlen], "Roundtrip failed for '{}'", orig);

        let comprlevel = 100 - ((100 * comprlen) / input.len().max(1)); // avoid zero-div
        if comprlevel < 0 {
            println!("'{}' enlarged by {}%", orig, -comprlevel);
        } else {
            println!("'{}' compressed by {}%", orig, comprlevel);
        }
    }

    println!("Encrypting and decrypting 1,000,000 test strings...");
    // C used random() with non-determin seed; Rust can use a seeded PRNG for repeatability.
    let mut rng = StdRng::seed_from_u64(0x22fa_acd5_cc1d_1234);
    let charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvxyz/. ";

    for _ in 0..1_000_000 {
        // random length [0,512)
        let ranlen = rng.gen_range(0..512);
        let mut in_buf = vec![0u8; ranlen];
        for i in 0..ranlen {
            if rng.gen::<u32>() & 1 == 1 {
                in_buf[i] = charset[rng.gen_range(0..charset.len())];
            } else {
                in_buf[i] = rng.gen::<u8>();
            }
        }
        let mut out = vec![0u8; 4096];
        let mut d = vec![0u8; 4096];
        let comprlen = smaz_compress(&in_buf, &mut out)
            .expect("Compress failed on random input");
        let decomprlen = smaz_decompress(&out[..comprlen], &mut d)
            .expect("Decompress failed on random input");
        assert_eq!(ranlen, decomprlen, "Random roundtrip length mismatch");
        assert_eq!(&in_buf[..], &d[..decomprlen], "Random roundtrip mismatch");
        // Disabled: println!("{} -> {}", comprlen, decomprlen);
    }
    println!("TEST PASSED :)");
}