use serde_json::json;
use csv::Writer;
use tempfile::NamedTempFile;
use std::io::{Seek, SeekFrom, Read};

#[test]
fn test_json_to_csv() {
    // Prepare JSON data
    let records = vec![
        json!({"foo": 1, "bar": "X"}),
        json!({"foo": 2, "bar": "Y"}),
    ];

    // Write to tmp csv
    let mut tmpfile = NamedTempFile::new().unwrap();
    {
        let mut wtr = Writer::from_writer(&mut tmpfile);
        wtr.write_record(&["foo", "bar"]).unwrap();
        for v in records.iter() {
            let foo = v["foo"].to_string();
            let bar = v["bar"].as_str().unwrap();
            wtr.write_record(&[foo, bar.to_string()]).unwrap();
        }
        wtr.flush().unwrap();
    }
    // Check contents
    tmpfile.seek(SeekFrom::Start(0)).unwrap();
    let mut out = String::new();
    tmpfile.read_to_string(&mut out).unwrap();
    assert!(out.contains("foo,bar"));
    assert!(out.contains("1,X")); 
    assert!(out.contains("2,Y"));
}