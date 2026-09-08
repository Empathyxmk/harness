use swansonk14_p_tqdm::VERSION;
use swansonk14_p_tqdm::p_tqdm::*;

/// Version test, verifies module's version symbol and info.
#[test]
fn test_version() {
    assert!(!VERSION.is_empty());
    assert_eq!(VERSION, "1.4.2");
}

/// Sequential: add 1 to each element.
#[test]
fn test_sequential() {
    fn f(x: &i32) -> i32 {
        x + 1
    }
    let out = _sequential_single(f, &[1, 2, 3]);
    assert_eq!(out, vec![2, 3, 4]);
}

/// Sequential with two iterables, add element-wise.
#[test]
fn test_sequential_multiple() {
    fn f(a: &i32, b: &i32) -> i32 {
        a + b
    }
    let out = _sequential_double(f, &[1, 2], &[2, 3]);
    assert_eq!(out, vec![3, 5]);
}

/// Sequential, test elementwise summing.
#[test]
fn test_sequential_length() {
    fn f(x: &i32, y: &i32) -> i32 {
        x + y
    }
    let out = _sequential_double(f, &[1, 2], &[5, 10]);
    assert_eq!(out, vec![6, 12]);
}

/// Sequential with empty iterable
#[test]
fn test_sequential_with_empty() {
    fn f(x: &i32) -> i32 {
        *x
    }
    let out = _sequential_single(f, &[]);
    assert_eq!(out, vec![]);
}

#[test]
#[should_panic]
fn test_sequential_with_exception() {
    fn f(x: &i32) -> i32 {
        if *x == 2 {
            panic!("bad");
        }
        x + 1
    }
    let _ = _sequential_single(f, &[1, 2, 3]);
}