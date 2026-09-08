use wjcryptlib::*;

#[test]
fn test_aesblock_edge_cases() {
    // Decrypt with invalid flag and differing key/iv/block lengths
    let args1 = ["-D", "00112233445566778899aabbccddeeff", "112233445566778899aabbccddeeff"];
    assert!(aesblock::run_command(&args1).is_err());
    let args2 = [
        "-D",
        "00112233445566778899aabbccddeeff",
        "1234567890abcdef1234567890abcdef",
    ];
    assert!(aesblock::run_command(&args2).is_ok());
}

#[test]
fn test_aesctr_edge_cases() {
    let args1 = [
        "00112233445566778899aabbccddeeff",
        "1234567890abcdef",
        "1",
    ];
    assert!(aesctroutput::run_command(&args1).is_ok());
    let args2 = [
        "00112233445566778899aabbccddeeff",
        "1234567890abcdef",
        "28",
    ];
    assert!(aesctroutput::run_command(&args2).is_ok());
}

#[test]
fn test_aesofb_normal_case() {
    let args = [
        "00112233445566778899aabbccddeeff",
        "1234567890abcdef",
        "8",
    ];
    assert!(aesofboutput::run_command(&args).is_ok());
}

#[test]
fn test_md5_and_sha1_empty_string() {
    let md5_hash = md5string::calculate_hash("");
    assert_eq!(
        md5_hash,
        "d41d8cd98f00b204e9800998ecf8427e",
        "Empty string MD5"
    );
    let sha1_hash = sha1string::calculate_hash("");
    assert_eq!(
        sha1_hash,
        "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "Empty string SHA1"
    );
}

#[test]
fn test_md5_and_sha1_long_string() {
    let longstr = "a".repeat(512);
    let md5_hash = md5string::calculate_hash(&longstr);
    assert_eq!(md5_hash, "079342a7fa4c94b83b4c1381f713bb85");
    let sha1_hash = sha1string::calculate_hash(&longstr);
    assert_eq!(sha1_hash, "1d5b3f7967b3e832be6b8c4baa0b2580228e5d75");
}