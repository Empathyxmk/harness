use sha2::{Sha512, Digest};

#[test]
fn test_sha512_hello_world_alternate() {
    let input = "hello world";
    let mut hasher = Sha512::new();
    hasher.update(input.as_bytes());
    let result = hasher.finalize();
    let hex = hex::encode(result);
    let expected = "309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f";
    assert_eq!(hex, expected, "SHA512 public test (alt) failed");
}