mod public_vdso {
    use ayeks_sgx_hardware::vdso::public::*;
    #[test]
    fn test_print_vdso_enumeration() {
        print_vdso_enumeration();
    }
}