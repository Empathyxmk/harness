use std::fs::{File, remove_file};
use std::io::{Write, Read};

#[test]
fn test_public_fake_vault_file() {
    let vault_file_path = "public_vaultfile";
    let mut file = File::create(vault_file_path).unwrap();
    write!(file, "$ANSIBLE_VAULT;1.1;AES256\ntestpublic").unwrap();
    let mut content = String::new();
    File::open(vault_file_path).unwrap().read_to_string(&mut content).unwrap();
    assert!(content.contains("$ANSIBLE_VAULT"));
    assert!(content.contains("public"));
    remove_file(vault_file_path).unwrap();
}

#[test]
fn test_public_vault_password() {
    let pw_file_path = "public_vaultpass";
    let vault_password = "superpublicpw";
    let mut file = File::create(pw_file_path).unwrap();
    write!(file, "{vault_password}").unwrap();
    let mut read_content = String::new();
    File::open(pw_file_path).unwrap().read_to_string(&mut read_content).unwrap();
    assert_eq!(read_content, vault_password);
    remove_file(pw_file_path).unwrap();
}

#[test]
fn test_public_multiple_vault_files() {
    let files = vec![
        ("vault_varied1.public", "$ANSIBLE_VAULT;1.2;AES256\npublicvaultcipher"),
        ("vault_varied2.public", "$ANSIBLE_VAULT;1.2;AES256\nanotherpubliccipher"),
    ];
    for (fname, vault_content) in files {
        let mut file = File::create(fname).unwrap();
        write!(file, "{vault_content}").unwrap();
        let mut read_content = String::new();
        File::open(fname).unwrap().read_to_string(&mut read_content).unwrap();
        assert!(read_content.contains("AES256"));
        remove_file(fname).unwrap();
    }
}