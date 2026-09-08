use spectre_poc::*;

#[test]
fn test_victim_function_valid() {
    // Original test used x = 0
    let x = 0;
    unsafe {
        victim_function(x);
    }
    println!("[test_victim_function_valid] Success");
}

#[test]
fn test_victim_function_invalid() {
    // Original test used x = array1_size
    unsafe {
        let x = ARRAY1_SIZE;
        victim_function(x);
    }
    println!("[test_victim_function_invalid] Success");
}

#[test]
fn test_victim_function_edge() {
    // Original test used x = array1_size - 1
    unsafe {
        let x = ARRAY1_SIZE - 1;
        victim_function(x);
    }
    println!("[test_victim_function_edge] Success");
}