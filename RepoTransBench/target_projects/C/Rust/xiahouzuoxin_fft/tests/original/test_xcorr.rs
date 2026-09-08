// Translation of tests/test_xcorr.c to Rust

use xiahouzuoxin_fft::*;
use std::cell::RefCell;

const CH_NUM: usize = 3;
const FIFO_SIZE: usize = 32;
const FIFO_SIZE_DIV2: usize = 16;

thread_local! {
    static X: RefCell<[[Complex; FIFO_SIZE]; CH_NUM]> = RefCell::new([[Complex{real:0.0, imag:0.0}; FIFO_SIZE]; CH_NUM]);
}

// Simulated PEAK_CHECK test logic
fn peak_check_test() -> (i32, f32) {
    let mut max: f32 = 0.0;
    let mut delay: i32 = 0;
    let ch = 0;
    X.with(|x_arr| {
        let mut x = x_arr.borrow_mut();
        for i in 0..FIFO_SIZE {
            x[0][i].real = i as f32;
            x[0][i].imag = 0.0;
        }
        max = x[ch][0].real.powi(2) + x[ch][0].imag.powi(2);
        delay = 0;
        for i in 1..5 {
            let temp = x[ch][i].real.powi(2) + x[ch][i].imag.powi(2);
            if temp > max { max = temp; delay = i as i32; }
        }
        for i in ((FIFO_SIZE-4)..FIFO_SIZE).rev() {
            let temp = x[ch][i].real.powi(2) + x[ch][i].imag.powi(2);
            if temp > max { max = temp; delay = i as i32; }
        }
        if delay > FIFO_SIZE_DIV2 as i32 {
            delay -= FIFO_SIZE as i32;
        }
    });
    (delay, max)
}

// Translate Gaussian rand (Box-Muller). This RNG is deterministic only if seed is fixed!
fn gauss_rand_seq(n: usize, seed: u64) -> Vec<f32> {
    use rand::{Rng, SeedableRng};
    use rand::rngs::StdRng;
    let mut rng = StdRng::seed_from_u64(seed);
    let mut out = Vec::new();
    let mut v1 = 0.0f32;
    let mut v2 = 0.0f32;
    let mut s = 0.0f32;
    let mut phase = 0;
    while out.len() < n {
        if phase == 0 {
            loop {
                let u1 = rng.gen::<f32>();
                let u2 = rng.gen::<f32>();
                v1 = 2.0 * u1 - 1.0;
                v2 = 2.0 * u2 - 1.0;
                s = v1 * v1 + v2 * v2;
                if s < 1.0 && s != 0.0 { break; }
            }
            out.push( v1 * ( -2.0 * s.ln() / s ).sqrt() );
        } else {
            out.push( v2 * ( -2.0 * s.ln() / s ).sqrt() );
        }
        phase = 1 - phase;
    }
    out
}

#[test]
fn test_dummy_peak_check() {
    let (delay, max) = peak_check_test();
    assert_eq!(delay, -1);
    assert!((max - 961.0).abs() < 1e-2);
}

#[test]
fn test_guass_rand() {
    // We use a fixed PRNG seed for deterministic output
    let res = gauss_rand_seq(20, 12345);
    assert_eq!(res.len(), 20);
    // Not asserting actual values (as C rand() and Rust PRNG will differ), just check statistical shape
    let mean = res.iter().cloned().sum::<f32>() / (res.len() as f32);
    assert!(mean.abs() < 1.0);
    let stddev = (res.iter().map(|x| (*x - mean).powi(2)).sum::<f32>() / (res.len() as f32)).sqrt();
    assert!(stddev > 0.5 && stddev < 2.5);
}