mod public_rdmsr {
    use ayeks_sgx_hardware::rdmsr::public::*;

    #[test]
    fn test_native_rdmsr_valid() {
        let mut lo = 0u32;
        let mut hi = 0u32;
        native_rdmsr(0x99, Some(&mut lo), Some(&mut hi));
        assert_eq!(lo, 0x99 ^ 0xAAAAAAAA, "low value wrong");
        assert_eq!(hi, 0x99 ^ 0x55555555, "high value wrong");
    }

    #[test]
    fn test_native_rdmsr_null() {
        native_rdmsr(0xBB, None, None);
    }

    #[test]
    fn test_print_rdmsr_enumeration() {
        print_rdmsr_enumeration();
    }
}