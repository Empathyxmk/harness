mod cpuid {
    use ayeks_sgx_hardware::cpuid::*;
    #[test]
    fn test_native_cpuid32_valid() {
        let mut eax = 0u32;
        let mut ebx = 0u32;
        let mut ecx = 0u32;
        let mut edx = 0u32;
        native_cpuid32(Some(&mut eax), Some(&mut ebx), Some(&mut ecx), Some(&mut edx));
        assert_eq!(eax, 0xDEADBEEF, "eax wrong");
        assert_eq!(ebx, 0xBEEFDEAD, "ebx wrong");
        assert_eq!(ecx, 0xABCD1234, "ecx wrong");
        assert_eq!(edx, 0x56789DEF, "edx wrong");
    }

    #[test]
    fn test_native_cpuid32_null() {
        // Should not panic if None
        native_cpuid32(None, None, None, None);
    }

    #[test]
    fn test_cpuid_max_basic() {
        assert_eq!(cpuid_max_basic(), 2);
    }

    #[test]
    fn test_print_cpuid_enumeration() {
        print_cpuid_enumeration();
    }
}