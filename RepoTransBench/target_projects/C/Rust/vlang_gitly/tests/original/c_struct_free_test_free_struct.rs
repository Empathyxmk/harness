// Translated from v_install/v/vlib/v/tests/c_struct_free/test_free_struct.c

#[cfg(test)]
mod tests {
    #[derive(Default)]
    struct Foo {
        free: i32,
    }

    #[test]
    fn test_struct_foo_field() {
        let mut f = Foo::default();
        f.free = 12345;
        assert_eq!(f.free, 12345);
    }
}