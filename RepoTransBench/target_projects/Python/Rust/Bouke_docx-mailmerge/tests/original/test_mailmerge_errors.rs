use std::io::Cursor;
use zip::result::ZipError;
use zip::ZipWriter;

#[test]
fn test_mailmerge_ctor_invalid_zip() {
    use zip::read::ZipArchive;

    let broken = Cursor::new(&b"notazipfile"[..]);
    let maybe_result: Result<ZipArchive<Cursor<&[u8]>>, ZipError> =
        ZipArchive::new(broken);

    assert!(maybe_result.is_err());
}

#[test]
fn test_mailmerge_ctor_content_types_missing() {
    // Simulate a minimal .docx file in memory missing [Content_Types].xml
    use zip::write::FileOptions;
    use std::io::Seek;
    use std::io::Write;

    let mut buf: Vec<u8> = Vec::new();
    {
        let mut w = ZipWriter::new(Cursor::new(&mut buf));
        w.start_file("word/document.xml", FileOptions::default()).unwrap();
        w.write_all(b"<doc/>").unwrap();
        w.finish().unwrap();
    }
    let mut reader = Cursor::new(buf);
    let result = zip::read::ZipArchive::new(&mut reader);

    assert!(result.is_ok(), "Should be able to open zip file (even if missing file)");

    // Now, simulate that opening '[Content_Types].xml' would Err
    let mut za = result.unwrap();
    let r = za.by_name("[Content_Types].xml");
    assert!(r.is_err(), "Should error because [Content_Types].xml is missing");
}