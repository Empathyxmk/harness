// Translated from v_install/v/vlib/v/tests/c_array_public_test.c

#[cfg(test)]
mod tests {
    fn gen_c_array(size: usize) -> Vec<u8> {
        let mut c_array = Vec::with_capacity(size);
        for i in 0..size {
            c_array.push(((i * 2) & 0xFF) as u8);
        }
        c_array
    }

    fn gen_c_int_array(size: usize) -> Vec<i32> {
        let mut c_array = Vec::with_capacity(size);
        for i in 0..size {
            c_array.push((i as i32) * 3);
        }
        c_array
    }

    #[test]
    fn test_gen_c_array() {
        let n = 8;
        let arr = gen_c_array(n);
        for i in 0..n {
            assert_eq!(arr[i], ((i * 2) & 0xFF) as u8);
        }
        // Spot check
        assert_eq!(arr[1], 2);
        assert_eq!(arr[n - 1], (((n - 1) * 2) & 0xFF) as u8);
    }

    #[test]
    fn test_gen_c_int_array() {
        let n = 6;
        let arr = gen_c_int_array(n);
        for i in 0..n {
            assert_eq!(arr[i], (i as i32) * 3);
        }
        // Spot check
        assert_eq!(arr[2], 6);
        assert_eq!(arr[n - 1], ((n - 1) as i32) * 3);
    }
}