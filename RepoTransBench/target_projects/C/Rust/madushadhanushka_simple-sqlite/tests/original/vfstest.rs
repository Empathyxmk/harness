use tempfile::NamedTempFile;
use std::io::{Write, Seek, SeekFrom, Read};

#[test]
fn test_vfs() {
    // Step 1: Open a new file
    let mut file = NamedTempFile::new().expect("create temp file");
    let path = file.path().to_str().unwrap().to_string();

    // Step 2: Seek offset 0 and write data
    let value_to_write = b"hello this is vfs test";
    file.as_file_mut().seek(SeekFrom::Start(0)).unwrap();
    file.as_file_mut().write_all(&value_to_write[..22]).unwrap();

    // Step 3: Seek offset 6 and read 4 bytes
    file.as_file_mut().seek(SeekFrom::Start(6)).unwrap();
    let mut read_buffer = [0u8; 4];
    file.as_file_mut().read_exact(&mut read_buffer).unwrap();
    assert_eq!(std::str::from_utf8(&read_buffer).unwrap(), "this");

    // Step 4: Overwrite offset 11 with "is override"
    file.as_file_mut().seek(SeekFrom::Start(11)).unwrap();
    let override_bytes = b"is override";
    file.as_file_mut().write_all(&override_bytes[..11]).unwrap();

    // Seek offset 0 and read back all 22 bytes
    file.as_file_mut().seek(SeekFrom::Start(0)).unwrap();
    let mut final_result = [0u8; 22];
    file.as_file_mut().read_exact(&mut final_result).unwrap();
    assert_eq!(
        std::str::from_utf8(&final_result).unwrap(),
        "hello this is override"
    );

    // Step 5: Close (drops on scope exit); remove file
    let file_path = file.path().to_path_buf();
    drop(file);
    assert!(std::fs::remove_file(&file_path).is_ok());
    assert!(!file_path.exists());
}