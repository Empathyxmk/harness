mod rdmsr {
    use ayeks_sgx_hardware::rdmsr::*;
    #[test]
    fn test_native_rdmsr_valid() {
        let mut lo = 0u32;
        let mut hi = 0u32;
        native_rdmsr(0x44, Some(&mut lo), Some(&mut hi));
        assert_eq!(lo, 0x44 ^ 0x80808080, "low value wrong");
        assert_eq!(hi, 0x44 ^ 0x10101010, "hi value wrong");
    }

    #[test]
    fn test_native_rdmsr_null() {
        native_rdmsr(0x55, None, None);
    }

    #[test]
    fn test_print_rdmsr_enumeration() {
        print_rdmsr_enumeration();
    }
}