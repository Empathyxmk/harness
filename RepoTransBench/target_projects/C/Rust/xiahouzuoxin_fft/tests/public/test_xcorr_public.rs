// Translation of tests/test_xcorr_public.c to Rust

use xiahouzuoxin_fft::*;
use std::cell::RefCell;

const CH_NUM: usize = 3;
const FIFO_SIZE: usize = 32;
const FIFO_SIZE_DIV2: usize = 16;

thread_local! {
    static X: RefCell<[[Complex; FIFO_SIZE]; CH_NUM]> = RefCell::new([[Complex{real:0.0, imag:0.0}; FIFO_SIZE]; CH_NUM]);
}

#[test]
fn dummy_peak_check_pub() {
    let ch = 1;
    X.with(|x_arr| {
        let mut x = x_arr.borrow_mut();
        // Fill ch 1 with reverse
        for i in 0..FIFO_SIZE {
            x[1][i].real = (FIFO_SIZE as i32 - 1 - i as i32) as f32;
            x[1][i].imag = 0.0;
        }
        let mut max = x[ch][0].real*x[ch][0].real + x[ch][0].imag*x[ch][0].imag;
        let mut delay = 0;
        for i in 1..10 {
            let temp = x[ch][i].real*x[ch][i].real + x[ch][i].imag*x[ch][i].imag;
            if temp > max { max = temp; delay = i; }
        }
        for i in (FIFO_SIZE-9..FIFO_SIZE).rev() {
            let temp = x[ch][i].real*x[ch][i].real + x[ch][i].imag*x[ch][i].imag;
            if temp > max { max = temp; delay = i; }
        }
        let mut peak_idx = delay as i32;
        if peak_idx > FIFO_SIZE_DIV2 as i32 {
            peak_idx -= FIFO_SIZE as i32;
        }
        assert_eq!(peak_idx, 0);
        assert!((max - 961.0).abs() < 1e-2);
    });
}

#[test]
fn dummy_conj_pub() {
    X.with(|x_arr| {
        let mut x = x_arr.borrow_mut();
        for i in 0..FIFO_SIZE {
            x[0][i].real = (i % 5) as f32;
            x[0][i].imag = ((i % 3) as i32 - 1) as f32;
            x[2][i].real = ((FIFO_SIZE - 1 - i) % 7) as f32;
            x[2][i].imag = ((i % 4) as i32 - 2) as f32;
        }
        let idx = 15;
        let conj_real = x[0][idx].real * x[2][idx].real + x[0][idx].imag * x[2][idx].imag;
        let conj_imag = x[0][idx].real * x[2][idx].imag - x[0][idx].imag * x[2][idx].real;
        assert!((conj_real + 1.0).abs() < 1e-2);
        assert!((conj_imag - 2.0).abs() < 1e-2);
    });
}