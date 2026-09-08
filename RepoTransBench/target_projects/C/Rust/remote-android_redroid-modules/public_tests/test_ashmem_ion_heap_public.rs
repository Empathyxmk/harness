use redroid_modules::ashmem::ion::{vmap, vunmap, PAGE_SIZE};

#[test]
fn test_ion_heap_functions_public() {
    // Public test: map+unmap 2 pages instead of 1
    let v = vmap(None, 2, 0, 0); // Using 2 pages instead of 1
    
    // Check allocation worked
    assert!(!v.is_null(), "PUBLIC vmap failed to allocate");
    println!("PUBLIC vmap 2 pages simulated ok");
    
    // Free the allocation
    vunmap(v);
    println!("PUBLIC vunmap simulated ok");
}