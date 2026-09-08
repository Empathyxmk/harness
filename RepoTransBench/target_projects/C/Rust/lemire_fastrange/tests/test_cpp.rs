use lemire_fastrange::*;
use std::collections::HashSet;
use rand::{Rng, thread_rng};

// Helper to mimic the rand() function behavior from the C++ test
fn get32rand() -> u32 {
    let mut rng = thread_rng();
    rng.gen::<u32>() ^ (rng.gen::<u32>() << 15) ^ (rng.gen::<u32>() << 30)
}

fn get64rand() -> u64 {
    ((get32rand() as u64) << 32) | get32rand() as u64
}

fn fill(number: usize) -> bool {
    let mut set = HashSet::new();
    while set.len() < number {
        set.insert(fastrangesize(get64rand(), number));
    }
    true
}

#[test]
fn test_cpp_functionality() {
    // Test fastrange32 and fastrange64 for a range of values
    for x in 0..1000000u32 {
        assert!(fastrange32(x, 5) < 5);
    }
    
    for x in 0..1000000u64 {
        assert!(fastrange64(x, 5) < 5);
    }
    
    // Only test a subset of the fill operation to keep test runtime reasonable
    for x in 1..100 {
        assert!(fill(x));
    }
}