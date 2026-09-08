// Rust translation of operatingsystem_c/chap07_synchronization/test_bounded_buffer_extra.c

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
            return -1;
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
    fn test_buffer_wraps_around() {
        unsafe {
            TEST_IN = 0;
            TEST_OUT = 0;
        }
        // Insert up to wrap
        for i in 0..(BUFFER_SIZE * 2) {
            test_insert_item(i as i32);
        }

        unsafe {
            assert_eq!(TEST_IN, 0);
        }
        // Remove all items
        let mut val = 0;
        for _i in 0..BUFFER_SIZE {
            test_remove_item(&mut val);
        }

        unsafe {
            assert_eq!(TEST_OUT, 0);
        }
    }

    #[test]
    fn test_overflow_protection() {
        unsafe {
            TEST_IN = 0;
            TEST_OUT = 0;
        }
        // Only allows BUFFER_SIZE elements
        for i in 0..BUFFER_SIZE {
            test_insert_item(i as i32);
        }

        // Should be full (simulate), next insert just wraps (simulate classic buffer wrap logic)
        test_insert_item(100);

        let mut outval = 0;
        test_remove_item(&mut outval); // Remove one

        unsafe {
            assert_eq!(TEST_OUT, 1);
        }
    }
}