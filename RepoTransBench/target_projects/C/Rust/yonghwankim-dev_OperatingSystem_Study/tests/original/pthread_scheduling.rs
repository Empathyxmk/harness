// Rust translation of operatingsystem_c/chap05_cpu-scheduling/test_pthread_scheduling.c

use std::sync::{Arc, Mutex};

static mut SUM: i32 = 0;

// Equivalent to: int sum; void* runner(void*);
fn runner(_arg: Option<()>) -> Option<()> {
    unsafe {
        SUM = 5;
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_runner_adds() {
        unsafe {
            SUM = 0;
        }
        runner(None);
        unsafe {
            assert_eq!(SUM, 5);
        }
    }
}