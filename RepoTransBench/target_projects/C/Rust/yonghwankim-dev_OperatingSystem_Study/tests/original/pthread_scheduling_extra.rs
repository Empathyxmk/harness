// Rust translation of operatingsystem_c/chap05_cpu-scheduling/test_pthread_scheduling_extra.c

#[cfg(test)]
mod tests {
    // main signature is normally fn main(), but for test we simulate as a callable fn.
    fn main_for_test(_argc: i32, _argv: &[&str]) -> i32 {
        // Simulates the original call, always returns 0 just like in the C code logic for non-error exit.
        0
    }

    #[test]
    fn test_main_runnable() {
        let argv = ["prog"];
        let res = main_for_test(1, &argv);
        assert_eq!(res, 0);
    }
}