// Translation of tests/unit/test_init.c

use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    static ref INITTED: Mutex<i32> = Mutex::new(0);
}

fn init() {
    let mut initted = INITTED.lock().unwrap();
    *initted = 1;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init_call() {
        *INITTED.lock().unwrap() = 0;
        init();
        assert_eq!(*INITTED.lock().unwrap(), 1);
    }
}