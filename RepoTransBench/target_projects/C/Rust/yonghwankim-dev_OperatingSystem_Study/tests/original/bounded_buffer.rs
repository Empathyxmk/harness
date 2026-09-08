// Rust translation of operatingsystem_c/chap07_synchronization/test_bounded_buffer.c

const BUFFER_SIZE: usize = 5;
static mut TEST_BUFFER: [i32; BUFFER_SIZE] = [0; BUFFER_SIZE];
static mut TEST_IN: usize = 0;
static mut TEST_OUT: usize = 0;

fn test_insert_item(item: i32) {
    unsafe {
        TEST_BUFFER[TEST_IN] = item;
        TEST_IN = (TEST_IN + 1) % BUFFER_SIZE;
    }
}

fn test_remove_item(item: &mut i32) -> i32 {
    unsafe {
        if TEST_IN == TEST_OUT {
            return -1; // Empty
        }
        *item = TEST_BUFFER[TEST_OUT];
        TEST_OUT = (TEST_OUT + 1) % BUFFER_SIZE;
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_insert_remove_fn() {
        unsafe {
            TEST_IN = 0;
            TEST_OUT = 0;
        }
        let val = 42;
        test_insert_item(val);

        unsafe {
            assert_eq!(TEST_IN, 1);
            assert_eq!(TEST_BUFFER[0], 42);
        }

        let mut outval = 0;
        let res = test_remove_item(&mut outval);

        assert_eq!(res, 0);
        assert_eq!(outval, 42);
        unsafe {
            assert_eq!(TEST_OUT, 1);
        }
    }

    #[test]
    fn test_empty_remove_fn() {
        unsafe {
            TEST_IN = 0;
            TEST_OUT = 0;
        }
        let mut outval = 0;
        let res = test_remove_item(&mut outval);

        assert_eq!(res, -1);
    }
}