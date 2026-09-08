use codeplea_genann_rs::*;
use std::fs::File;
use std::io::{Write, Read, BufReader};
use std::path::Path;

#[test]
fn public_preset_read() {
    // Expects "example/xor.ann" exists as in C example
    let save_name = "example/xor.ann";
    let exists = Path::new(save_name).exists();
    if !exists {
        eprintln!("Couldn't open file: {}", save_name);
        // skip this test if file does not exist
        return;
    }
    let mut saved = File::open(save_name).unwrap();
    let ann = genann_read(&mut saved);
    if ann.is_none() {
        panic!("Error loading ANN from file: {}.", save_name);
    }
    let mut ann = ann.unwrap();

    let input: [[f64; 2]; 4] = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ];
    for i in 0..4 {
        println!(
            "Output for [{}, {}] is {}.",
            input[i][0], input[i][1], ann.run(Some(&input[i]))[0]
        );
    }
}