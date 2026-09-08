use ndarray::prelude::*;
use crate::benchmarks::*;
use std::collections::HashMap;

#[test]
fn test_fast_npss_same() {
    let a = ArrayD::from_shape_fn(vec![3,60,5], |_| rand::random::<f64>());
    let score = fast_npss(&a, &a);
    assert!((score - 0.0).abs() < 1e-8);
}

#[test]
fn test_fast_npss_different_nan_guard() {
    let a = ArrayD::from_elem(vec![2,8,2], 1.0);
    let b = ArrayD::from_elem(vec![2,8,2], 0.0);
    let score = fast_npss(&a, &b);
    assert!(score.is_nan());
}

#[test]
fn test_flatjoints() {
    let x = Array4::<f64>::zeros((2,3,4,5));
    let y = flatjoints(&x);
    assert_eq!(y.shape(), &[2,3,20]);
}

fn make_fake_fk(joints: usize, frames: usize, rand: bool) -> (Array4<f64>, Array4<f64>, Array3<f64>, Array3<f64>, Array4<f64>, Vec<i32>) {
    let (x, q) = if rand {
        (
            Array4::<f64>::random((1, frames, joints, 3), rand::distributions::Standard),
            Array4::<f64>::random((1, frames, joints, 4), rand::distributions::Standard)
        )
    } else {
        (
            Array4::<f64>::zeros((1, frames, joints, 3)),
            Array4::from_elem((1, frames, joints, 4), 1.0)
        )
    };
    let x_mean = Array3::<f64>::zeros((1, joints*3, 1));
    let x_std = Array3::<f64>::ones((1, joints*3, 1));
    let offsets = Array4::<f64>::zeros((1, 1, joints, 3));
    let mut parents = vec![-1];
    parents.extend((0..(joints-1)).map(|i| i as i32));
    (x, q, x_mean, x_std, offsets, parents)
}

#[test]
fn test_benchmark_interpolation_various() {
    let examples = vec![(22,65), (5,20)];
    for (j, frames) in examples {
        let (x, q, x_mean, x_std, offsets, parents) = make_fake_fk(j, frames, false);
        if j == 22 {
            let results = benchmark_interpolation(&x, &q, &x_mean, &x_std, &offsets, &parents, None, 10, 10).unwrap();
            assert!(results.contains_key("zero_velocity"));
            assert!(results.contains_key("interpolation"));
        } else {
            let err = benchmark_interpolation(&x, &q, &x_mean, &x_std, &offsets, &parents, None, 1, 1);
            assert!(err.is_err());
        }
    }
}

#[test]
fn test_benchmark_interpolation_nan_guard() {
    let x = Array4::<f64>::zeros((1,30,5,3));
    let q = Array4::<f64>::zeros((1,30,5,4));
    let x_mean = Array3::<f64>::zeros((1, 15, 1));
    let x_std = Array3::<f64>::ones((1, 15, 1));
    let offsets = Array4::<f64>::zeros((1, 1, 5, 3));
    let parents = vec![-1,0,1,2,3];
    let _ = benchmark_interpolation(&x, &q, &x_mean, &x_std, &offsets, &parents, None, 1, 1);
}