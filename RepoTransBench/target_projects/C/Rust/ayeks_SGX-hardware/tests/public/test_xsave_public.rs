mod public_xsave {
    use ayeks_sgx_hardware::xsave::public::*;
    #[test]
    fn test_print_XSAVE_enumeration() {
        print_XSAVE_enumeration();
    }
}