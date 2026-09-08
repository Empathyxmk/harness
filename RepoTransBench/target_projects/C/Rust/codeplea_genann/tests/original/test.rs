use codeplea_genann_rs::*;
use std::fs::File;
use std::io::{Write, BufWriter, BufReader};
use std::time::Duration;

#[test]
fn basic() {
    let mut ann = Genann::new(1, 0, 0, 1).expect("basic ANN");

    assert_eq!(ann.total_weights, 2);

    let mut a = 0.0;
    ann.weight[0] = 0.0;
    ann.weight[1] = 0.0;
    assert!((0.5 - ann.run(Some(&[a]))[0]).abs() < 0.001);

    a = 1.0;
    assert!((0.5 - ann.run(Some(&[a]))[0]).abs() < 0.001);

    a = 11.0;
    assert!((0.5 - ann.run(Some(&[a]))[0]).abs() < 0.001);

    a = 1.0;
    ann.weight[0] = 1.0;
    ann.weight[1] = 1.0;
    assert!((0.5 - ann.run(Some(&[a]))[0]).abs() < 0.001);

    a = 10.0;
    ann.weight[0] = 1.0;
    ann.weight[1] = 1.0;
    // Output is forced to 1.0 for input 10
    assert!((1.0 - ann.run(Some(&[a]))[0]).abs() < 0.001);

    a = -10.0;
    assert!((0.0 - ann.run(Some(&[a]))[0]).abs() < 0.001);
}

#[test]
fn xor() {
    let mut ann = Genann::new(2, 1, 2, 1).unwrap();
    ann.activation_hidden = genann_act_threshold;
    ann.activation_output = genann_act_threshold;

    assert_eq!(ann.total_weights, 9);

    // First hidden
    ann.weight[0] = 0.5;
    ann.weight[1] = 1.0;
    ann.weight[2] = 1.0;

    // Second hidden
    ann.weight[3] = 1.0;
    ann.weight[4] = 1.0;
    ann.weight[5] = 1.0;

    // Output
    ann.weight[6] = 0.5;
    ann.weight[7] = 1.0;
    ann.weight[8] = -1.0;

    let input = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ];
    let output = [0.0, 1.0, 1.0, 0.0];

    for i in 0..4 {
        assert!((output[i] - ann.run(Some(&input[i]))[0]).abs() < 0.001);
    }
}

#[test]
fn backprop() {
    let mut ann = Genann::new(1, 0, 0, 1).unwrap();
    let input = 0.5;
    let output = 1.0;

    let first_try = ann.run(Some(&[input]))[0];
    ann.train(&[input], &[output], 0.5);
    let second_try = ann.run(Some(&[input]))[0];
    assert!((first_try - output).abs() > (second_try - output).abs() || (second_try - output).abs() < 1e-6);
}

#[test]
fn train_and() {
    let input = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ];
    let output = [0.0, 0.0, 0.0, 1.0];
    let mut ann = Genann::new(2, 0, 0, 1).unwrap();

    for _ in 0..50 {
        for j in 0..4 {
            ann.train(&input[j], &[output[j]], 0.8);
        }
    }
    ann.activation_output = genann_act_threshold;
    for j in 0..4 {
        assert!((output[j] - ann.run(Some(&input[j]))[0]).abs() < 0.001);
    }
}

#[test]
fn train_or() {
    let input = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ];
    let output = [0.0, 1.0, 1.0, 1.0];
    let mut ann = Genann::new(2, 0, 0, 1).unwrap();
    ann.randomize();
    for _ in 0..50 {
        for j in 0..4 {
            ann.train(&input[j], &[output[j]], 0.8);
        }
    }
    ann.activation_output = genann_act_threshold;
    for j in 0..4 {
        assert!((output[j] - ann.run(Some(&input[j]))[0]).abs() < 0.001);
    }
}

#[test]
fn train_xor() {
    let input = [
        [0.0, 0.0],
        [0.0, 1.0],
        [1.0, 0.0],
        [1.0, 1.0]
    ];
    let output = [0.0, 1.0, 1.0, 0.0];
    let mut ann = Genann::new(2, 1, 2, 1).unwrap();
    for _ in 0..500 {
        for j in 0..4 {
            ann.train(&input[j], &[output[j]], 3.0);
        }
    }
    ann.activation_output = genann_act_threshold;
    for j in 0..4 {
        assert!((output[j] - ann.run(Some(&input[j]))[0]).abs() < 0.001);
    }
}

#[test]
fn persist() {
    let ann = Genann::new(1000, 5, 50, 10).unwrap();
    let file_path = "persist.txt";
    {
        let mut out = File::create(file_path).unwrap();
        genann_write(&ann, &mut out);
    }
    let mut inp = File::open(file_path).unwrap();
    let ann2 = genann_read(&mut inp).unwrap();

    assert_eq!(ann.inputs, ann2.inputs);
    assert_eq!(ann.hidden_layers, ann2.hidden_layers);
    assert_eq!(ann.hidden, ann2.hidden);
    assert_eq!(ann.outputs, ann2.outputs);
    assert_eq!(ann.total_weights, ann2.total_weights);
    for i in 0..ann.total_weights {
        assert!((ann.weight[i] - ann2.weight[i]).abs() < 0.001);
    }
}

#[test]
fn copy() {
    let ann = Genann::new(1000, 5, 50, 10).unwrap();
    let ann2 = ann.copy();

    assert_eq!(ann.inputs, ann2.inputs);
    assert_eq!(ann.hidden_layers, ann2.hidden_layers);
    assert_eq!(ann.hidden, ann2.hidden);
    assert_eq!(ann.outputs, ann2.outputs);
    assert_eq!(ann.total_weights, ann2.total_weights);
    for i in 0..ann.total_weights {
        assert!((ann.weight[i] - ann2.weight[i]).abs() < 0.001);
    }
}

#[test]
fn sigmoid() {
    let mut i = -20.0;
    let max = 20.0;
    let d = 0.0001;
    let ann = Genann::new(1, 0, 0, 1).unwrap();
    while i < max {
        let v1 = genann_act_sigmoid(&ann, i);
        let v2 = genann_act_sigmoid_cached(&ann, i);
        assert!((v1 - v2).abs() < 1e-12);
        i += d;
    }
}