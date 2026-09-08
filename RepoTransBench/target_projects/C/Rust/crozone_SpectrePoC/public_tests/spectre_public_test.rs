use spectre_poc::*;

#[test]
fn test_victim_function_valid_public() {
    // Public test used x = 3
    let x = 3;
    unsafe {
        victim_function(x);
    }
    println!("[test_victim_function_valid_public] Success");
}

#[test]
fn test_victim_function_invalid_public() {
    // Public test used x = array1_size + 1
    unsafe {
        let x = ARRAY1_SIZE + 1;
        victim_function(x);
    }
    println!("[test_victim_function_invalid_public] Success");
}

#[test]
fn test_victim_function_edge_public() {
    // Public test used x = 1
    let x = 1;
    unsafe {
        victim_function(x);
    }
    println!("[test_victim_function_edge_public] Success");
}