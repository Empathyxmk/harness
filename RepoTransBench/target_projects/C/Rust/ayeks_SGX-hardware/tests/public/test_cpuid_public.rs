mod public_cpuid {
    use ayeks_sgx_hardware::cpuid::public::*;

    #[test]
    fn test_native_cpuid32_valid() {
        let mut eax = 0u32;
        let mut ebx = 0u32;
        let mut ecx = 0u32;
        let mut edx = 0u32;
        native_cpuid32(Some(&mut eax), Some(&mut ebx), Some(&mut ecx), Some(&mut edx));
        assert_eq!(eax, 0x1234ABCD, "eax wrong");
        assert_eq!(ebx, 0xDCBA4321, "ebx wrong");
        assert_eq!(ecx, 0xB16B00B5, "ecx wrong");
        assert_eq!(edx, 0xCAFEDADA, "edx wrong");
    }

    #[test]
    fn test_native_cpuid32_null() {
        native_cpuid32(None, None, None, None);
    }

    #[test]
    fn test_cpuid_max_basic() {
        assert_eq!(cpuid_max_basic(), 4);
    }

    #[test]
    fn test_print_cpuid_enumeration() {
        print_cpuid_enumeration();
    }
}