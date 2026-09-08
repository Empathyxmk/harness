use ayeks_sgx_hardware::*;

fn assert_true(expr: bool, msg: &str) {
    assert!(expr, "{}", msg);
}
fn assert_eq_i64(x: i64, y: i64, msg: &str) {
    assert_eq!(x, y, "{}: expected {} got {}", msg, y, x);
}

#[test]
fn test_cpuid_basic() {
    let mut eax = 0u32;
    let mut ebx = 0u32;
    let mut ecx = 0u32;
    let mut edx = 0u32;
    let ret = native_cpuid32(0, Some(&mut eax), Some(&mut ebx), Some(&mut ecx), Some(&mut edx));
    assert_eq_i64(ret as i64, 0, "native_cpuid32 returned nonzero");
    assert_eq_i64(eax as i64, 0x12345678, "EAX value wrong");
    assert_eq_i64(ebx as i64, 0x87654321, "EBX value wrong");
    assert_eq_i64(ecx as i64, 0xDEADBEEF, "ECX value wrong");
    assert_eq_i64(edx as i64, 0xBEEFDEAD, "EDX value wrong");
}

#[test]
fn test_cpuid_max_basic() {
    assert_eq!(
        cpuid_max_basic(), 0x16,
        "cpuid_max_basic"
    );
}

#[test]
fn test_cpuid_null_pointers() {
    // Should return -1 if any output ptr is None
    let ret = native_cpuid32(0, None, None, None, None);
    assert_eq!(ret, -1, "native_cpuid32 should fail on NULL");
}

#[test]
fn test_rdmsr_basic() {
    let mut lo = 0u32;
    let mut hi = 0u32;
    let ret = native_rdmsr(0, Some(&mut lo), Some(&mut hi));
    assert_eq!(ret, 0, "native_rdmsr returned nonzero");
    assert_eq!(lo, 0xAABBCCDD, "rdmsr lo wrong");
    assert_eq!(hi, 0x11223344, "rdmsr hi wrong");
}

#[test]
fn test_rdmsr_null_pointers() {
    let ret = native_rdmsr(0, None, None);
    assert_eq!(ret, -1, "native_rdmsr should fail on NULL");
}

#[test]
fn test_print_functions() {
    // For print statements, just ensure we can call them (will print to stdout)
    print_cpuid_enumeration();
    print_rdmsr_enumeration();
    print_vdso_enumeration();
    print_XSAVE_enumeration();
}