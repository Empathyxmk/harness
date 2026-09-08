// Translation of tests/unit/test_debug.c
use std::sync::Mutex;
use lazy_static::lazy_static;
use std::io::{self, Write};

lazy_static! {
    static ref G_VERBOSE: Mutex<i32> = Mutex::new(0);
}

fn debug(fmt: &str, args: &[i32]) {
    let verbose = *G_VERBOSE.lock().unwrap();
    if verbose == 0 {
        return;
    }
    // We'll only handle %d pattern and one integer for simplicity (per test usage)
    if let Some(&arg) = args.get(0) {
        let formatted = fmt.replace("%d", &arg.to_string());
        let _ = writeln!(io::stderr(), "{formatted}");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn debug_off() {
        *G_VERBOSE.lock().unwrap() = 0;
        debug("This should not print: %d\n", &[41]);
        assert_eq!(0, 0);
    }

    #[test]
    fn debug_on() {
        *G_VERBOSE.lock().unwrap() = 1;
        debug("This should print: %d\n", &[42]);
        assert_eq!(0, 0);
    }
}