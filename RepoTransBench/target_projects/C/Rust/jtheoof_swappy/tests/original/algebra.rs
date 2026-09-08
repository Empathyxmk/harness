use swappy::algebra::{gaussian_kernel, gaussian_kernel_free};

#[test]
fn test_gaussian_kernel_basic() {
    let width = 3;
    let sigma = 1.0;
    let kernel = gaussian_kernel(width, sigma);

    assert!(!kernel.kernel.is_empty());
    assert_eq!(kernel.size, (width * width + 1) as usize);
    assert!(kernel.sum > 0.0);
    assert!((kernel.sigma - sigma).abs() < 1e-6);
}

#[test]
fn test_gaussian_kernel_free_null() {
    gaussian_kernel_free(None);
    // In Rust we just verify it doesn't panic
}