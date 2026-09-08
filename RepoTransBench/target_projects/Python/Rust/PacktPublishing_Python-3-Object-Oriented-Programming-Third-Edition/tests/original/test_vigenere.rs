use python3_oop_rust::vigenere_cipher::VigenereCipher;

#[test]
fn test_encryption() {
    let cipher = VigenereCipher::new("KEY");
    let encrypted = cipher.encrypt("HELLO WORLD");
    assert_eq!(encrypted, "RIJVS UYVJN");
}

#[test]
fn test_decryption() {
    let cipher = VigenereCipher::new("KEY");
    let decrypted = cipher.decrypt("RIJVS UYVJN");
    assert_eq!(decrypted, "HELLO WORLD");
}

#[test]
fn test_nonalpha() {
    let cipher = VigenereCipher::new("KEY");
    let encrypted = cipher.encrypt("123!@#");
    assert_eq!(encrypted, "123!@#");
}