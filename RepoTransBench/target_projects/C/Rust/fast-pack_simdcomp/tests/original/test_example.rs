// Translated from C: tests/test_example.c

use simdcomp::*;

#[test]
fn test_simd_pack_unpack() {
    // Test maxbits_length, simdpack_length, simdpack_compressedbytes, simdunpack_length
    let n = 128;
    let mut datain = vec![0u32; n];
    for i in 0..n {
        datain[i] = i as u32;
    }

    let b = maxbits_length(&datain, n);
    let compressed_bytes = simdpack_compressedbytes(n, b);
    let mut buffer = vec![0u8; compressed_bytes];

    let howmanybytes = simdpack_length(&datain, n, &mut buffer, b);
    assert!(
        howmanybytes <= compressed_bytes,
        "Used more bytes than estimated!"
    );

    // Check decompress
    let mut backbuffer = vec![0u32; n];
    simdunpack_length(&buffer, n, &mut backbuffer, b);
    for i in 0..n {
        assert_eq!(
            datain[i], backbuffer[i],
            "Original and decompressed values differ at index {}",
            i
        );
    }

    // Try error case: 0-length
    let mut d = [123u32; 1];
    let mut buf = [0u8; 64];
    // Should simply return offset 0, i.e. no write/read.
    let e = simdpack_length(&d, 0, &mut buf, 1);
    assert_eq!(e, 0, "Pack offset for 0-length should be 0");
    // Should not panic
    simdunpack_length(&buf, 0, &mut d, 1);
}