mod vdso {
    use ayeks_sgx_hardware::vdso::*;
    #[test]
    fn test_print_vdso_enumeration() {
        print_vdso_enumeration();
    }
}