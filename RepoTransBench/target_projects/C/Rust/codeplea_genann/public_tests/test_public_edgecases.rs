use codeplea_genann_rs::*;
use std::fs::File;
use std::io::{Write, Read};
use std::path::Path;

#[test]
fn public_edgecases() {
    // Construct with more neurons and layers than in original edge case
    let mut ann = Genann::new(3, 2, 4, 2).expect("valid public ANN");
    // Test all neuron outputs on zero-initialized input should be consistent
    let input1 = [0.0, 1.0, -1.0];
    let out1 = ann.run(Some(&input1));

    // Public edge: train on a single unusual data case
    let train_in = [0.5, 0.2, 0.8];
    let train_out = [0.9, 0.1];
    ann.train(&train_in, &train_out, 1.9);
    // Confirm outputs change after training
    let out2 = ann.run(Some(&train_in));

    // Output for sanity: not asserting values, as the actual values vary
    println!(
        "Sanity: output1 = [{}, {}], output2 = [{}, {}]",
        out1[0], out1[1], out2[0], out2[1]
    );

    // Check network struct invariants after operations
    assert_eq!(ann.inputs, 3);
    assert_eq!(ann.outputs, 2);
    assert_eq!(ann.hidden_layers, 2);
    assert_eq!(ann.hidden, 4);

    // Test: freeing (dropping) already freed is no-op in Rust (but simulate API)
    drop(ann); // first free
    // Repeated drop (via explicit None) is safe
    let ann: Option<Genann> = None;
    drop(ann);

    // Passing None as input to run, should not crash, returns out buffer
    let mut ann = Genann::new(1, 0, 0, 1).unwrap();
    let o = ann.run(None);
    assert!(o.len() > 0);
}