use tempfile::NamedTempFile;
use std::collections::HashMap;
use std::io::{Read, Seek, SeekFrom, Write};

// A simulation of a simple Pager in Rust.
struct Pager {
    pages: HashMap<u32, Vec<u8>>,
    page_size: usize,
}
impl Pager {
    fn new(page_size: usize) -> Self {
        Pager { pages: HashMap::new(), page_size }
    }
    fn get(&mut self, pgno: u32) -> &mut Vec<u8> {
        self.pages.entry(pgno).or_insert(vec![0u8; self.page_size])
    }
    fn commit(&self, _file: &mut std::fs::File) {
        // Would write pages to disk in real implementation
    }
    fn rollback(&mut self, backup: &HashMap<u32, Vec<u8>>) {
        self.pages = backup.clone();
    }
    fn page_count(&self) -> usize {
        self.pages.len()
    }
}

#[test]
fn test_pager() {
    let page_size = 32;
    let mut pager = Pager::new(page_size);

    // Step 1: Open file and create three pages
    let mut file = NamedTempFile::new().unwrap();

    // Step 2: Write data into three pages and commit
    let pages_and_data = [
        (1u32, b"Page One" as &[u8]),
        (2u32, b"Page Two"),
        (3u32, b"Page Three"),
    ];
    for (pgno, data) in &pages_and_data {
        let ppage = pager.get(*pgno);
        ppage[..data.len()].copy_from_slice(data);
    }

    // Step 3: Read pages, check contents
    let mut zbuf = vec![0u8; page_size];
    for (pgno, data) in &pages_and_data {
        let ppage = pager.get(*pgno);
        zbuf[..ppage.len()].copy_from_slice(ppage);
        let s = std::str::from_utf8(&zbuf[..data.len()]).unwrap();
        assert_eq!(
            s,
            std::str::from_utf8(data).unwrap(),
            "Page {} read content matches",
            pgno
        );
    }

    // Step 4: Write to page 3, then rollback before commit
    let backup = pager.pages.clone();
    let ppage3 = pager.get(3u32);
    let newdata = b"Page test rollback";
    ppage3[..newdata.len()].copy_from_slice(newdata);

    // Rollback
    pager.rollback(&backup);

    // Check page 3 matches original content
    let ppage3 = pager.get(3u32);
    let zbuf = &ppage3[..b"Page Three".len()];
    assert_eq!(std::str::from_utf8(zbuf).unwrap(), "Page Three");

    // Page count
    assert_eq!(pager.page_count(), 3);

    // Clean up
    let path = file.into_temp_path();
    path.close().unwrap();
}