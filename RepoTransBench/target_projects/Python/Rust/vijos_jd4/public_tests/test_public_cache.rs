use tempfile::TempDir;
use std::fs::{self, File};
use std::io::{Read, Write};
use vijos_jd4::cache::{cache_open, cache_invalidate};

#[tokio::test]
async fn test_public_cache_open_file_found() {
    let tmp_dir = TempDir::new().unwrap();
    let domain = "domX";
    let pid = "probz";
    let domain_dir = tmp_dir.path().join(domain);
    fs::create_dir_all(&domain_dir).unwrap();
    let file_path = domain_dir.join(format!("{}.zip", pid));
    fs::write(&file_path, b"newdata").unwrap();

    let mut f = cache_open(None, domain, pid).await.unwrap();
    let mut data = Vec::new();
    f.read_to_end(&mut data).unwrap();
    assert_eq!(&data, b"newdata");
}

#[tokio::test]
async fn test_public_cache_open_download() {
    let tmp_dir = TempDir::new().unwrap();
    let domain = "domY";
    let pid = "pz0";
    let mut file = cache_open(None, domain, pid).await.unwrap();
    let mut content = Vec::new();
    file.read_to_end(&mut content).unwrap();
    assert_eq!(&content, b"probdata");
}

#[tokio::test]
async fn test_public_cache_invalidate() {
    let tmp_dir = TempDir::new().unwrap();
    let domain = "domZ";
    let pid = "ppq";
    let cachedir = tmp_dir.path().join(domain);
    fs::create_dir_all(&cachedir).unwrap();
    let fpath = cachedir.join(format!("{}.zip", pid));
    fs::write(&fpath, b"z").unwrap();

    cache_invalidate(domain, pid).await.unwrap();
    assert!(!fpath.exists());
    cache_invalidate(domain, pid).await.unwrap();
}