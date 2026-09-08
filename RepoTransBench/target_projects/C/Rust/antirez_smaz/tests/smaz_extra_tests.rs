//! Rust port of the extra original edge/corner-case test suite (smaz_extra_tests.c)
use smaz::{smaz_compress, smaz_decompress};
use std::ffi::CStr;

fn round_trip(input: &[u8]) -> bool {
    let mut comp = [0u8; 2048];
    let mut decomp = [0u8; 2048];
    let clen = match smaz_compress(input, &mut comp) { Ok(x) => x, Err(_) => return false };
    let dlen = match smaz_decompress(&comp[..clen], &mut decomp) { Ok(x) => x, Err(_) => return false };
    &decomp[..dlen] == input
}

#[test]
fn extra_smaz_tests() {
    // Test: Null input/length 0
    let mut buf = [0u8; 512];
    let ret = smaz_compress(b"", &mut buf);
    println!("Compress empty: {}", matches!(ret, Ok(0)));

    // Output buffer too small for compression
    let mut tiny = [0u8; 1];
    let ret = smaz_compress(b"abc", &mut tiny);
    println!("Compress too small output: {}", matches!(ret, Err(_)));

    // Output buffer too small for decompression
    let mut comp = [0u8; 512];
    let clen = smaz_compress(b"hello world", &mut comp).unwrap();
    let ret = smaz_decompress(&comp[..clen], &mut tiny);
    println!("Decompress too small output: {}", matches!(ret, Err(_)));

    // Long uncompressible string
    let mut longstr = [b'z'; 299];
    let ret = round_trip(&longstr);
    println!("Long string round-trip: {}", ret);

    // Non-ASCII/binary data
    let binary = [0, 1, 2, 3, 0xfe, 0xff, 0x00];
    let ret = round_trip(&binary);
    println!("Binary round-trip: {}", ret);

    // Normal English
    let english = b"The quick brown fox jumps over the lazy dog";
    let ret = round_trip(english);
    println!("English sentence round-trip: {}", ret);

    // Output buffer exactly right for decompression
    let clen = smaz_compress(b"test", &mut buf).unwrap();
    let mut recon = [0u8; 8];
    let ret = smaz_decompress(&buf[..clen], &mut recon);
    println!("Exactly sized out buffer: {}", matches!(ret, Ok(n) if n == 4));

    // Malformed decompress input
    let fake = [99u8,99,99,99];
    let ret = smaz_decompress(&fake, &mut buf);
    println!("Malformed decompress: {}", matches!(ret, Err(_)));

    // Input that's almost a dictionary word
    let nearword = b"thee";
    let ret = round_trip(nearword);
    println!("Near dictionary word: {}", ret);

    // Edge: Output buffer size = 0
    let mut zero = [0u8; 0];
    let ret = smaz_compress(b"foo", &mut zero);
    println!("Compress zero out buf: {}", matches!(ret, Err(_)));

    let clen = smaz_compress(b"nonempty", &mut buf).unwrap();
    let ret = smaz_decompress(&buf[..clen], &mut zero);
    println!("Decompress zero out buf: {}", matches!(ret, Err(_)));

    // Edge: Large compressible text
    let multi = b"This is is is is is is is is is is a test.";
    let ret = round_trip(multi);
    println!("Highly compressible: {}", ret);

    // Edge: Long inputs that match exactly the dict word length
    let dictword = b"the";
    let ret = round_trip(dictword);
    println!("Dictionary word match: {}", ret);

    // Input with punctuation
    let punct = b",.?!";
    let ret = round_trip(punct);
    println!("Punctuation coverage: {}", ret);

    println!("All extra tests completed.");
}