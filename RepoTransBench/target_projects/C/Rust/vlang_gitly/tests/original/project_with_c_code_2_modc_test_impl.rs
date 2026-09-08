// Translated from v_install/v/vlib/v/tests/project_with_c_code_2/modc/test_impl.c

#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Atype {
        val: i32,
    }

    fn new_atype(n: i32) -> Box<Atype> {
        Box::new(Atype { val: n })
    }

    fn handle_array(arr: &mut [Atype]) {
        // In C: just consume array for test coverage.
        for e in arr.iter_mut() {
            e.val += 0; // no-op, but touch mut ref for test
        }
    }

    fn handle_array2(arr: &mut [Atype]) {
        // In C: similar, but pointer-to-array; here we just work with ref again.
        for e in arr.iter_mut() {
            e.val += 0;
        }
    }

    fn destroy_atype(_p: Box<Atype>) {
        // Drop handled by Box
    }

    #[test]
    fn test_new_and_destroy_atype() {
        let obj = new_atype(13);
        assert_eq!(obj.val, 13);
        destroy_atype(obj);
    }

    #[test]
    fn test_handle_array() {
        let mut arr = [Atype { val: 1 }, Atype { val: 2 }];
        handle_array(&mut arr);
    }

    #[test]
    fn test_handle_array2() {
        let mut arr = [Atype { val: 5 }, Atype { val: 10 }];
        handle_array2(&mut arr);
    }
}