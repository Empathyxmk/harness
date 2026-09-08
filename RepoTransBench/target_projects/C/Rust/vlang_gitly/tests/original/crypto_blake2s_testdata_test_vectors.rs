// Translated from v_install/v/vlib/crypto/blake2s/testdata/test_vectors.v (Parts 1/6 + more expected)
//
// This test suite checks the Blake2s hash implementation against a battery of reference
// vectors for numerous input sizes. This Rust test does NOT implement the full hash algorithm,
// instead it provides the assertion structure and uses the 'blake2' crate for actual hashing.
//
// If your Rust crate or lib implements its own blake2s, replace 'blake2' with your own call.

extern crate hex;
extern crate blake2;

use blake2::{Blake2s, Digest};

#[derive(Debug)]
struct TestVector {
    input: &'static str,
    key:   &'static str,
    output: &'static str,
}

fn hexstr_to_bytes(hexstr: &str) -> Vec<u8> {
    if hexstr.is_empty() {
        vec![]
    } else {
        hex::decode(hexstr).unwrap()
    }
}

#[test]
fn test_blake2s_reference_vectors_unkeyed() {
    let vectors = [
        TestVector { input:  "", key:  "", output: "69217a3079908094e11121d042354a7c1f55b6482ca1a51e1b250dfd1ed0eef9" },
        TestVector { input:  "00", key:  "", output: "e34d74dbaf4ff4c6abd871cc220451d2ea2648846c7757fbaac82fe51ad64bea" },
        TestVector { input:  "0001", key:  "", output: "ddad9ab15dac4549ba42f49d262496bef6c0bae1dd342a8808f8ea267c6e210c" },
        TestVector { input:  "000102", key:  "", output: "e8f91c6ef232a041452ab0e149070cdd7dd1769e75b3a5921be37876c45c9900" },
        TestVector { input:  "00010203", key:  "", output: "0cc70e00348b86ba2944d0c32038b25c55584f90df2304f55fa332af5fb01e20" },
        TestVector { input:  "0001020304", key:  "", output: "ec1964191087a4fe9df1c795342a02ffc191a5b251764856ae5b8b5769f0c6cd" },
        TestVector { input:  "000102030405", key:  "", output: "e1fa51618d7df4eb70cf0d5a9e906f806e9d19f7f4f01e3b621288e4120405d6" },
        TestVector { input:  "00010203040506", key:  "", output: "598001fafbe8f94ec66dc827d012cfcbba2228569f448e89ea2208c8bf769293" },
        TestVector { input:  "0001020304050607", key:  "", output: "c7e887b546623635e93e0495598f1726821996c2377705b93a1f636f872bfa2d" },
        TestVector { input:  "000102030405060708", key:  "", output: "c315a437dd28062a770d481967136b1b5eb88b21ee53d0329c5897126e9db02c" },
        TestVector { input:  "00010203040506070809", key:  "", output: "bb473deddc055fea6228f207da575347bb00404cd349d38c18026307a224cbff" },
        TestVector { input:  "000102030405060708090a", key:  "", output: "687e1873a8277591bb33d9adf9a13912efefe557cafc39a7952623e47255f16d" },
        TestVector { input:  "000102030405060708090a0b", key:  "", output: "1ac7ba754d6e2f94e0e86c46bfb262abbb74f450ef456d6b4d97aa80ce6da767" },
        TestVector { input:  "000102030405060708090a0b0c", key:  "", output: "012c97809614816b5d9494477d4b687d15b96eb69c0e8074a8516f31224b5c98" },
        TestVector { input:  "000102030405060708090a0b0c0d", key:  "", output: "91ffd26cfa4da5134c7ea262f7889c329f61f6a657225cc212f40056d986b3f4" },
        TestVector { input:  "000102030405060708090a0b0c0d0e", key:  "", output: "d97c828d8182a72180a06a78268330673f7c4e0635947c04c02323fd45c0a52d" },
        TestVector { input:  "000102030405060708090a0b0c0d0e0f", key:  "", output: "efc04cdc391c7e9119bd38668a534e65fe31036d6a62112e44ebeb11f9c57080" },
        TestVector { input:  "000102030405060708090a0b0c0d0e0f10", key:  "", output: "992cf5c053442a5fbc4faf583e04e50bb70d2f39fbb6a503f89e56a63e18578a" },
        TestVector { input:  "000102030405060708090a0b0c0d0e0f1011", key:  "", output: "38640e9f21983e67b539caccae5ecf615ae2764f75a09c9c59b76483c1fbc735" },
        TestVector { input:  "000102030405060708090a0b0c0d0e0f101112", key:  "", output: "213dd34c7efe4fb27a6b35f6b4000d1fe03281af3c723e5c9f94747a5f31cd3b" },
        // ... Add all remaining TestVector entries from the C/V file (see rest of split file!) --
    ];

    for vector in &vectors {
        // Convert hex string input
        let input_bytes = hexstr_to_bytes(vector.input);

        // Note: we only handle unkeyed test vectors in this test.
        assert!(vector.key.is_empty(), "Keyed vectors not expected in this test batch");

        // Compute hash
        let mut hasher = Blake2s::new();
        hasher.update(&input_bytes);
        let result = hasher.finalize();
        let result_hex = hex::encode(result);

        assert_eq!(
            result_hex, vector.output,
            "Failed on input='{}' expected output '{}', got '{}'",
            vector.input, vector.output, result_hex
        );
    }
}

// Note: Complete the list of TestVector items for the rest of the file parts. For brevity,
// only the first batch is implemented; extend with the remaining reference vectors in
// subsequent translation operations or batches.