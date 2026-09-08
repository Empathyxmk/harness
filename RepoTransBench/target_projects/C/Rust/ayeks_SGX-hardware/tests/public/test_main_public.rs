mod public_api {
    use ayeks_sgx_hardware::lib_public as api;

    fn assert_eq_u32(x: u32, y: u32, msg: &str) {
        assert_eq!(x, y, "{}: expected {} got {}", msg, y, x);
    }

    #[test]
    fn test_native_cpuid32_valid() {
        let mut eax = 0u32;
        let mut ebx = 0u32;
        let mut ecx = 0u32;
        let mut edx = 0u32;
        let ret = api::native_cpuid32(0, Some(&mut eax), Some(&mut ebx), Some(&mut ecx), Some(&mut edx));
        assert_eq!(ret, 0, "cpuid32 returned nonzero");
        assert_eq_u32(eax, 0x89ABCDEF, "cpuid32 eax different");
        assert_eq_u32(ebx, 0xFEDCBA98, "cpuid32 ebx different");
        assert_eq_u32(ecx, 0xCAFEBABE, "cpuid32 ecx different");
        assert_eq_u32(edx, 0xBAADF00D, "cpuid32 edx different");
    }

    #[test]
    fn test_cpuid_max_basic() {
        assert_eq!(
            api::cpuid_max_basic(), 0x18,
            "cpuid_max_basic mismatch"
        );
    }

    #[test]
    fn test_native_rdmsr_valid() {
        let mut lo = 0u32;
        let mut hi = 0u32;
        api::native_rdmsr(0x55, Some(&mut lo), Some(&mut hi));
        assert_eq_u32(lo, 0x55 ^ 0xF0F0F0F0, "rdmsr lo incorrect");
        assert_eq_u32(hi, 0x55 ^ 0x0F0F0F0F, "rdmsr hi incorrect");
    }

    #[test]
    fn test_native_rdmsr_null() {
        api::native_rdmsr(0xAA, None, None);
    }

    #[test]
    fn test_print_functions() {
        api::print_cpuid_enumeration();
        api::print_rdmsr_enumeration();
        api::print_vdso_enumeration();
        api::print_XSAVE_enumeration();
    }
}