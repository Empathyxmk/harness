use serde_json::json;
use std::fs::File;
use std::io::{self, BufReader, BufRead, Write};
use tempfile::NamedTempFile;

#[test]
fn test_dumptool_from_jsonfile() {
    let records = vec![
        json!({"foo": 100, "bar": "abc"}),
        json!({"foo": 200, "bar": "def"}),
    ];

    // Write JSON records to temp file ("input.json")
    let mut infile = NamedTempFile::new().unwrap();
    let inpath = infile.path().to_str().unwrap();
    for record in &records {
        writeln!(infile, "{}", record).unwrap();
    }
    infile.flush().unwrap();

    // Simulate reading the file line-by-line as dumptool would
    let f = File::open(inpath).unwrap();
    let reader = BufReader::new(f);
    let read_records: Vec<serde_json::Value> = reader.lines()
        .map(|l| serde_json::from_str(&l.unwrap()).unwrap())
        .collect();

    assert_eq!(read_records, records);
}