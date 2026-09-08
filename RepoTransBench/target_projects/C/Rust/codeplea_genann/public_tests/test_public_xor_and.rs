use codeplea_genann_rs::*;
use rand::Rng;
use std::time::{SystemTime, UNIX_EPOCH};

#[test]
fn public_xor_and() {
    println!("GENANN public test: Train on AND function.");
    // Seed with time to randomize weights, as in C code
    let t = SystemTime::now().duration_since(UNIX_EPOCH).unwrap();
    let mut rng = rand::thread_rng();

    let input: [[f64;2];4] = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0],
    ];
    let output = [0.0, 0.0, 0.0, 1.0];
    // 2 inputs, 1 hidden layer of 2, 1 output
    let mut ann = Genann::new(2, 1, 2, 1).unwrap();

    // Train repeatedly
    for _ in 0..500 {
        for j in 0..4 {
            ann.train(&input[j], &[output[j]], 2.5);
        }
    }
    // Print results
    for i in 0..4 {
        println!(
            "Output for [{}, {}] is {}.",
            input[i][0], input[i][1], ann.run(Some(&input[i]))[0]
        );
    }
}