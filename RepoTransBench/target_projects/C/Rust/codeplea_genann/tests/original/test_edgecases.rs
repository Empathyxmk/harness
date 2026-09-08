use codeplea_genann_rs::*;
use std::fs::File;
use std::io::{Write, Read};
use std::path::Path;

#[test]
fn test_invalid_inits() {
    let ann = Genann::new(0, 1, 2, 1);
    assert!(ann.is_none());

    let ann = Genann::new(2, -1, 2, 1);
    assert!(ann.is_none());

    let ann = Genann::new(2, 1, 2, 0);
    assert!(ann.is_none());

    let ann = Genann::new(2, 1, 0, 1);
    assert!(ann.is_none());
}

#[test]
fn test_copy_random_free() {
    let ann = Genann::new(2, 1, 2, 1).expect("valid ANN");
    let copy = ann.copy();
    assert_ne!(&ann as *const _, &copy as *const _);

    let mut ann2 = ann.clone();
    ann2.randomize();

    let changed = ann2.weight.iter()
        .zip(copy.weight.iter())
        .any(|(a,b)| a != b);
    assert!(changed);
    // free simulated via drop
}

#[test]
fn test_activations() {
    let mut ann = Genann::new(2, 1, 2, 1).unwrap();
    // Use the fn pointers from lib
    ann.activation_hidden = genann_act_sigmoid;
    ann.activation_output = genann_act_sigmoid;

    // Sigmoid extreme values
    let t = genann_act_sigmoid(&ann, -100.0);
    assert!(t >= 0.0 && t < 0.01);
    let t = genann_act_sigmoid(&ann, 100.0);
    assert!(t > 0.99 && t <= 1.0);

    let val0 = genann_act_sigmoid(&ann, 0.0);
    assert!(val0 > 0.0 && val0 < 1.0);

    let t = genann_act_threshold(&ann, -1.0);
    assert_eq!(t as i32, 0);
    let t = genann_act_threshold(&ann, 1.0);
    assert_eq!(t as i32, 1);
    let t = genann_act_linear(&ann, 5.0);
    assert_eq!(t as i32, 5);
}

#[test]
fn test_file_io() {
    let ann = Genann::new(2, 1, 2, 1).unwrap();
    let file_path = "test.ann";
    {
        let mut f = File::create(file_path).expect("create");
        genann_write(&ann, &mut f);
    }

    let mut f = File::open(file_path).expect("open");
    let read_ann = genann_read(&mut f).expect("ANN read");
    assert_eq!(ann.inputs, read_ann.inputs);
    assert_eq!(ann.outputs, read_ann.outputs);
    assert_eq!(ann.hidden_layers, read_ann.hidden_layers);
    assert_eq!(ann.hidden, read_ann.hidden);

    drop(f);
    std::fs::remove_file(file_path).expect("delete");

    // Try to read a corrupt file
    let broken_file = "test_broken.ann";
    {
        let mut f = File::create(broken_file).expect("create broken");
        let _ = f.write_all(b"corrupt-data");
    }
    let mut f = File::open(broken_file).unwrap();
    let broken = genann_read(&mut f);
    assert!(broken.is_none());
    drop(f);
    std::fs::remove_file(broken_file).unwrap();
}