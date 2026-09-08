use redroid_modules::ashmem::{VmAreaStruct, deps};
use redroid_modules::binder;

// Mock implementation for public tests - returns different value
fn mock_shmem_zero_setup_public(_vma: &VmAreaStruct) -> i32 {
    2024 // Changed return value for public test
}

// Override the kallsyms_lookup_name function for testing
fn public_test_kallsyms_lookup_name(name: &str) -> Option<fn(&VmAreaStruct) -> i32> {
    if name == "shmem_zero_setup" {
        Some(mock_shmem_zero_setup_public)
    } else {
        None
    }
}

#[test]
fn test_shmem_zero_setup_public() {
    // Replace the kallsyms_lookup_name function
    let original = binder::kallsyms_lookup_name;
    std::mem::replace(&mut binder::kallsyms_lookup_name, public_test_kallsyms_lookup_name);
    
    // Reset the static variable for clean test
    unsafe { deps::SHMEM_ZERO_SETUP_PTR = None; }
    
    // Create test structure with specified values
    let vma = VmAreaStruct { dummy: 123, other: 999 };
    
    // First call should initialize the static ptr
    let result1 = deps::shmem_zero_setup(&vma);
    
    // Second call should use the cached pointer
    let result2 = deps::shmem_zero_setup(&vma);
    
    // Verify results - public test expects 2024, not 42!
    assert_eq!(result1, 2024, "First call should return 2024");
    assert_eq!(result2, 2024, "Second call should return 2024");
    
    println!("ashmem/deps.c: shmem_zero_setup static/cache branch PUBLIC PASS");
    
    // Restore the original function
    std::mem::replace(&mut binder::kallsyms_lookup_name, original);
}