//! Test support helpers for original/manual tests

pub fn read_lines(filename: &str) -> Vec<String> {
    use std::fs::File;
    use std::io::{BufRead, BufReader};
    let file = File::open(filename).expect("unable to open file");
    BufReader::new(file)
        .lines()
        .map(|l| l.expect("unable to read line"))
        .collect()
}