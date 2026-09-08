use std::fs::File;
use std::io::{BufRead, BufReader};

#[test]
fn test_test_fastq_reads() {
    // Open test FASTQ for parsing and sanity check
    let path = "tests/data/test.fastq";
    let file = File::open(path).expect("Cannot open test FASTQ for reading");
    let reader = BufReader::new(file);
    let mut line_count = 0;
    let mut seq_name_lines = 0;
    let mut qq_count = 0;
    for line in reader.lines() {
        let l = line.expect("Read line");
        line_count += 1;
        if l.starts_with('@') {
            seq_name_lines += 1;
        }
        if l.starts_with('+') {
            qq_count += 1
        }
    }
    // Basic expectation: every sequence should have @, + headers
    assert!(seq_name_lines > 0);
    assert_eq!(seq_name_lines, qq_count);
    // FASTQ should be a multiple of 4 lines per record
    assert_eq!(line_count % 4, 0, "FASTQ not multiple of 4 lines");
}