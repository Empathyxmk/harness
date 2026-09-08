use wjcryptlib::*;

#[test]
fn test_md5_string_abc() {
    let hash = md5string::calculate_hash("abc");
    assert_eq!(
        &hash,
        "900150983cd24fb0d6963f7d28e17f72",
        "MD5 hash for 'abc' failed"
    );
}

#[test]
fn test_sha1_string_abc() {
    let hash = sha1string::calculate_hash("abc");
    assert_eq!(
        &hash,
        "a9993e364706816aba3e25717850c26c9cd0d89d",
        "SHA1 hash for 'abc' failed"
    );
}

#[test]
fn test_sha256_string_abc() {
    let hash = sha256string::calculate_hash("abc");
    assert_eq!(
        &hash,
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
    );
}

#[test]
fn test_sha512_string_abc() {
    let hash = sha512string::calculate_hash("abc");
    assert_eq!(
        &hash,
        "ddaf35a193617abacc417349ae20413112e6fa4e89a97ea20a9eeee64b55d39a2192992a274fc1a836ba3c23a3feebbd454d4423643ce80e2a9ac94fa54ca49f",
        "SHA512 hash for 'abc' failed"
    );
}

#[test]
fn test_rc4output_simple() {
    let (rc4out, _dropped) = rc4output::rc4_with_drop("1234567890abcdef", 16, 0);
    assert_eq!(rc4out.len(), 16);
}

#[test]
fn test_aesblock_encrypt_and_decrypt_block() {
    let pt = hex::decode("000102030405060708090a0b0c0d0e0f").unwrap();
    let key = hex::decode("0011223344556677").unwrap();
    let ct = aesblock::encrypt_block(&pt, &key, aesblock::CipherMode::ECB).unwrap();
    let pt2 = aesblock::decrypt_block(&ct, &key, aesblock::CipherMode::ECB).unwrap();
    assert_eq!(pt, pt2, "AESBlock encrypt/decrypt failed");
}

#[test]
fn test_aesctroutput_valid_call() {
    let key = "000102030405060708090a0b0c0d0e0f";
    let iv = "0001020304050607";
    let num_bytes = 16;
    let ct = aesctroutput::generate_output(&[key, iv, "16"]).unwrap();
    assert_eq!(ct.len(), 16);
}

#[test]
fn test_aesofboutput_valid_call() {
    let key = "000102030405060708090a0b0c0d0e0f";
    let iv = "0001020304050607";
    let num_bytes = 16;
    let ct = aesofboutput::generate_output(&[key, iv, "16"]).unwrap();
    assert_eq!(ct.len(), 16);
}