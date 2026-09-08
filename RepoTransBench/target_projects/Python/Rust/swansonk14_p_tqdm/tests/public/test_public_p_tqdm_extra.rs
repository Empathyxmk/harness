use swansonk14_p_tqdm::VERSION;
use swansonk14_p_tqdm::p_tqdm::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version_public() {
        assert!(!VERSION.is_empty());
        assert!(VERSION.chars().all(|c| c.is_ascii() || c == '.'));
        let ver = VERSION;
        let regex = regex::Regex::new(r"^\d+\.\d+\.\d+$").unwrap();
        assert!(regex.is_match(ver));
    }

    #[test]
    fn test_sequential_public() {
        fn f(x: &i32) -> i32 {
            x * 3
        }
        let out = _sequential_single(f, &[2, 4, 6]);
        assert_eq!(out, vec![6, 12, 18]);
    }

    #[test]
    fn test_sequential_multiple_public() {
        fn f(a: &i32, b: &i32) -> i32 {
            a * b
        }
        let out = _sequential_double(f, &[3, 4], &[5, 6]);
        assert_eq!(out, vec![15, 24]);
    }

    #[test]
    fn test_sequential_length_public() {
        fn f(x: &i32, y: &i32) -> i32 {
            x * y * 2
        }
        let out = _sequential_double(f, &[2, 3], &[7, 11]);
        assert_eq!(out, vec![28, 66]);
    }

    #[test]
    fn test_sequential_with_empty_public() {
        fn f(x: &i32) -> i32 {
            x * 10
        }
        let out = _sequential_single(f, &[]);
        assert_eq!(out, vec![]);
    }

    #[test]
    #[should_panic]
    fn test_sequential_with_exception_public() {
        fn f(x: &i32) -> i32 {
            if *x == 5 {
                panic!("terrible");
            }
            x * 2
        }
        let _ = _sequential_single(f, &[3, 5, 7]);
    }
}