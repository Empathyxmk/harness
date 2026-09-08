//! Rust translation of the public reference tests (smaz_public_test.c)
use smaz::{smaz_compress, smaz_decompress};

use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

#[test]
fn public_smaz_test_suite() {
    // Source test cases use alternate strings
    let strings = [
        "Another string for smaz testing",
        "zipzap",
        "A random test sentence",
        "Totally_different_example123",
        "Compression libraries like smaz test well",
        "To be, or not to be, that is the question",
        "testing SMAZ with random sentences for high coverage",
        "4321 numbers 5678 will 40 50 60 compress somewhat",
        "also, some additional spanish sentences:",
        "En un lugar de la Mancha, de cuyo nombre no quiero acordarme",
        "Mi vida es pura",
        "El creador de esta libreria vive en Madrid",
        "let's try some file paths",
        "/usr/local/bin/smaz",
        "https://openai.com/research",
        "https://github.com/example/smaz_public/test",
        "/mnt/data/music/Albums/Unusual"
    ];

    for orig in &strings {
        let input = orig.as_bytes();
        let mut out = [0u8; 4096];
        let mut d = [0u8; 4096];

        let comprlen = smaz_compress(input, &mut out)
            .expect("Compression failed in public_smaz_test");
        let decomprlen = smaz_decompress(&out[..comprlen], &mut d)
            .expect("Decompression failed in public_smaz_test");

        assert_eq!(input.len(), decomprlen, "Lengths did not match for '{}'", orig);
        assert_eq!(&input[..], &d[..decomprlen], "Roundtrip failed for '{}'", orig);

        let comprlevel = 100 - ((100 * comprlen) / input.len().max(1)); // avoid div0
        if comprlevel < 0 {
            println!("'{}' enlarged by {}%", orig, -comprlevel);
        } else {
            println!("'{}' compressed by {}%", orig, comprlevel);
        }
    }

    println!("Encrypting and decrypting 500,000 public test strings...");
    // Use consistent PRNG seed for reproducibility
    let mut rng = StdRng::seed_from_u64(0xa13e_dd2a_037c_2321);
    let charset = b"1234567890abcdefGHIJKLMNOPQRSTUVWXYZ/. ";

    for _ in 0..500_000 {
        let ranlen = rng.gen_range(0..256);
        let mut in_buf = vec![0u8; ranlen];
        for j in 0..ranlen {
            if rng.gen::<u32>() & 1 == 1 {
                in_buf[j] = charset[rng.gen_range(0..charset.len())];
            } else {
                in_buf[j] = rng.gen::<u8>() % 128; // ascii range only for public
            }
        }
        let mut out = vec![0u8; 4096];
        let mut d = vec![0u8; 4096];
        let comprlen = smaz_compress(&in_buf, &mut out)
            .expect("Compress failed on public random input");
        let decomprlen = smaz_decompress(&out[..comprlen], &mut d)
            .expect("Decompress failed on public random input");
        assert_eq!(ranlen, decomprlen, "Public random roundtrip length mismatch");
        assert_eq!(&in_buf[..], &d[..decomprlen], "Public random roundtrip mismatch");
        // println!("{} -> {}", comprlen, decomprlen); // For debugging
    }
    println!("PUBLIC TEST PASSED :)");
}