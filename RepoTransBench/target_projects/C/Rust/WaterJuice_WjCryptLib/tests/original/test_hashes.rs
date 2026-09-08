use md5::{Md5, Digest as Md5Digest};
use sha1::{Sha1, Digest as Sha1Digest};
use sha2::{Sha256, Sha512, Digest};
use hex::encode;

struct HashTestVector<'a> {
    plain: &'a str,
    md5: &'a str,
    sha1: &'a str,
    sha256: &'a str,
    sha512: &'a str,
}

const TEST_VECTORS: &[HashTestVector] = &[
    HashTestVector {
        plain: "",
        md5: "d41d8cd98f00b204e9800998ecf8427e",
        sha1: "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        sha256: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        sha512: "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
    },
    HashTestVector {
        plain: "a",
        md5: "0cc175b9c0f1b6a831c399e269772661",
        sha1: "86f7e437faa5a7fce15d1ddcb9eaeaaea377667b8",
        sha256: "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
        sha512: "1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbc8c12cfc7957b2652fe9a75",
    },
    HashTestVector {
        plain: "aaa",
        md5: "47bce5c74f58f4867dbd57e9ca9f808",
        sha1: "7e240de74fb1ed08fa08d38063f6a6a91462a815",
        sha256: "9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0",
        sha512: "d6f644b19812e97b5d871658d6d3400ecd4787faeb9b8990c1e7608288664be77257104a58d033bcf1a0e0945ff06468ebe53e2dff36e248424c7273117dac09",
    },
    HashTestVector {
        plain: "abc",
        md5: "900150983cd24fb0d6963f7d28e17f72",
        sha1: "a9993e364706816aba3e25717850c26c9cd0d89d",
        sha256: "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        sha512: "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f",
    },
    HashTestVector {
        plain: "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
        md5: "8215ef0796a20bcaaae116d3876c664a",
        sha1: "84983e441c3bd26ebaae4aa1f95129e5e54670f1",
        sha256: "248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1",
        sha512: "204a8fc6dda82f0a0ced7beb8e08a41657c16ef468b228a8279be331a703c33596fd15c13b1b07f9aa1d3bea57789ca031ad85c7a71dd70354ec631238ca3445",
    },
    HashTestVector {
        plain: "The quick brown fox jumps over the lazy dog",
        md5: "9e107d9d372bb6826bd81d3542a419d6",
        sha1: "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12",
        sha256: "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
        sha512: "07e547d9586f6a73f73fbac0435ed76951218fb7d0c8d788a309d785436bbb642e93a252a954f23912547d1e8a3b5ed6e1bfd7097821233fa0538f3db854fee6",
    },
    HashTestVector {
        plain: "The quick brown fox jumps over the lazy dog.",
        md5: "e4d909c290d0fb1ca068ffaddf22cbd0",
        sha1: "408d94384216f890ff7a0c3528e8bed1e0b01621",
        sha256: "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c",
        sha512: "91ea1245f20d46ae9a037a989f54f1f790f0a47607eeb8a14d12890cea77a1bbc6c7ed9cf205e67b7f2b8fd4c7dfd3a7a8617e45f3c463d481c7e586c39a1ed",
    },
    HashTestVector {
        plain: "message digest",
        md5: "f96b697d7cb7938d525a2f31aaf161d0",
        sha1: "c12252ceda8be8994d5fa0290a47231c1d16aae3",
        sha256: "f7846f55cf23e14eebeab5b4e1550cad5b509e3348fbc4efa3a1413d393cb650",
        sha512: "107dbf389d9e9f71a3a95f6c055b9251bc5268c2be16d6c13492ea45b0199f3309e16455ab1e96118e8a905d5597b72038ddb372a89826046de66687bb420e7c",
    },
    HashTestVector {
        plain: "abcdefghijklmnopqrstuvwxyz",
        md5: "c3fcd3d76192e4007dfb496cca67e13b",
        sha1: "32d10c7b8cf96570ca04ce37f2a19d84240d3a89",
        sha256: "71c480df93d6ae2f1efad1447c66c9525e316218cf51fc8d9ed832f2daf18b73",
        sha512: "4dbff86cc2ca1bae1e16468a05cb9881c97f1753bce3619034898faa1aabe429955a1bf8ec483d7421fe3c1646613a59ed5441fb0f321389f77f48a879c7b1f1",
    },
    HashTestVector {
        plain: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
        md5: "d174ab98d277d9f5a5611c2c9f419d9f",
        sha1: "761c457bf73b14d27e9e9265c46f4b4dda11f940",
        sha256: "db4bfcbd4da0cd85a60c3c37d3fbd8805c77f15fc6b1fdfe614ee0a7c8fdb4c0",
        sha512: "1e07be23c26a86ea37ea810c8ec7809352515a970e9253c26f536cfc7a9996c45c8370583e0a78fa4a90041d71a4ceab7423f19c71b9d5a3e01249f0bebd5894",
    },
    HashTestVector {
        plain: "12345678901234567890123456789012345678901234567890123456789012345678901234567890",
        md5: "57edf4a22be3c955ac49da2e2107b67a",
        sha1: "50abf5706a150990a08b2c5ea40fa0e585554732",
        sha256: "f371bc4a311f2b009eef952dd83c81453c8026c8e935592d0f9c308453c81e3e",
        sha512: "72ec1ef1124a45b047e8b7c75a932195135bb61de24ec0d1914042246e0aec3a2354e093d76f3048b456764346900cb130d2a4fd5dd16abb5e30bcb850dee843",
    },
];

// Helper to verify against reference hashes (hex string, lowercase, no whitespace).
fn hash_eq(result: &[u8], hexval: &str) -> bool {
    let hex_out = encode(result).to_lowercase();
    hex_out == hexval.to_lowercase()
}

#[test]
fn test_md5_hash_vectors() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Md5::new();
        hasher.update(v.plain.as_bytes());
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.md5),
            "Test vector {} failed (MD5): got {}, expected {}",
            i,
            encode(result),
            v.md5
        );
    }
}

#[test]
fn test_md5_hash_vectors_byte_by_byte() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Md5::new();
        for b in v.plain.as_bytes() {
            hasher.update(&[*b]);
        }
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.md5),
            "Test vector {} failed (MD5, bytewise): got {}, expected {}",
            i,
            encode(result),
            v.md5
        );
    }
}

#[test]
fn test_sha1_hash_vectors() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha1::new();
        hasher.update(v.plain.as_bytes());
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha1),
            "Test vector {} failed (SHA1): got {}, expected {}",
            i,
            encode(result),
            v.sha1
        );
    }
}

#[test]
fn test_sha1_hash_vectors_byte_by_byte() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha1::new();
        for b in v.plain.as_bytes() {
            hasher.update(&[*b]);
        }
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha1),
            "Test vector {} failed (SHA1, bytewise): got {}, expected {}",
            i,
            encode(result),
            v.sha1
        );
    }
}

#[test]
fn test_sha256_hash_vectors() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha256::new();
        hasher.update(v.plain.as_bytes());
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha256),
            "Test vector {} failed (SHA256): got {}, expected {}",
            i,
            encode(result),
            v.sha256
        );
    }
}

#[test]
fn test_sha256_hash_vectors_byte_by_byte() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha256::new();
        for b in v.plain.as_bytes() {
            hasher.update(&[*b]);
        }
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha256),
            "Test vector {} failed (SHA256, bytewise): got {}, expected {}",
            i,
            encode(result),
            v.sha256
        );
    }
}

#[test]
fn test_sha512_hash_vectors() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha512::new();
        hasher.update(v.plain.as_bytes());
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha512),
            "Test vector {} failed (SHA512): got {}, expected {}",
            i,
            encode(result),
            v.sha512
        );
    }
}

#[test]
fn test_sha512_hash_vectors_byte_by_byte() {
    for (i, v) in TEST_VECTORS.iter().enumerate() {
        let mut hasher = Sha512::new();
        for b in v.plain.as_bytes() {
            hasher.update(&[*b]);
        }
        let result = hasher.finalize();
        assert!(
            hash_eq(&result, v.sha512),
            "Test vector {} failed (SHA512, bytewise): got {}, expected {}",
            i,
            encode(result),
            v.sha512
        );
    }
}